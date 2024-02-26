import io
import os
from datetime import datetime
from os import path
from pathlib import Path
from urllib.parse import urljoin

import pyarrow.parquet as pq
from mage_ai.io.config import ConfigFileLoader
from mage_ai.io.postgres import Postgres
from mage_ai.settings.repo import get_repo_path
from pandas import DataFrame
from sqlalchemy import create_engine
from sqlalchemy.engine import URL

from magic_zoomcamp.utils.dtypes import taxi_dtypes, taxi_parse_dates

if "data_exporter" not in globals():
    from mage_ai.data_preparation.decorators import data_exporter
import pandas as pd
import requests
from google.cloud import storage

if "custom" not in globals():
    from mage_ai.data_preparation.decorators import custom
if "test" not in globals():
    from mage_ai.data_preparation.decorators import test


def get_file_from_web(service, date, session, source="original"):
    url_fname = f"{service}_tripdata_{date.strftime('%Y-%m')}"
    if source == "original":
        base_url = "https://d37ci6vzurychx.cloudfront.net/trip-data/"
        url_fpath = f"{url_fname}.parquet"
    else:
        base_url = "https://github.com/DataTalksClub/nyc-tlc-data/releases/download/"
        url_fpath = f"{service}/{url_fname}.csv.gz"
    url = urljoin(base_url, url_fpath)
    return session.get(url)


def get_files_from_web(service, date_range, session, source):
    for date in date_range:
        yield get_file_from_web(service, date, session, source)


def read_csv_iter(service, response_object_content, batch_size=10000):
    df_iter = pd.read_csv(
        io.BytesIO(response_object_content),
        dtype=taxi_dtypes[service],
        parse_dates=taxi_parse_dates[service],
        iterator=True,
        chunksize=batch_size,
        compression="gzip",
    )
    return df_iter


def transform_columns(service, df_iter):
    for df in df_iter:
        df.columns = df.columns.str.lower()
        yield df


def read_parquet_iter(response_object_content, batch_size):
    parquet_file = pq.ParquetFile(io.BytesIO(response_object_content))
    parquet_iter = parquet_file.iter_batches(batch_size=batch_size)
    return parquet_iter


def create_postgres_engine():
    url_object = URL.create(
        drivername="postgresql",
        database=os.environ["POSTGRES_DBNAME"],
        username=os.environ["POSTGRES_USER"],
        password=os.environ["POSTGRES_PASSWORD"],
        host=os.environ["POSTGRES_HOST"],
        port=int(os.environ["POSTGRES_PORT"]),
    )
    engine = create_engine(url_object)
    return engine


def export_to_postgres(idx, df, table_name, engine, is_replace=False):
    if idx == 0 and is_replace:
        df.head(n=0).to_sql(
            name=table_name, con=engine, if_exists="replace", index=False
        )
        print("Created table")
    df.to_sql(name=table_name, con=engine, if_exists="append", index=False)
    print(f"inserted another chunk")


def export_data_to_postgres(
    service,
    response_object,
    batch_size,
    table_name,
    engine,
    source="original",
    is_replace=False,
):
    data = response_object.content
    if source != "original":
        csv_iter = read_csv_iter(service, data, batch_size)
        df_iter = transform_columns(service, csv_iter)
    else:
        df_iter = read_parquet_iter(data, batch_size)
    for idx, df in enumerate(df_iter):
        export_to_postgres(idx, df, table_name, engine, is_replace)


@custom
def web_to_postgres(*args, **kwargs):
    """
    args: The output from any upstream parent blocks (if applicable)

    Returns:
        Anything (e.g. data frame, dictionary, array, int, str, etc.)
    """
    # Specify your custom logic here
    service = kwargs["service"]
    year = kwargs["year"]
    source = kwargs["source"]
    batch_size = kwargs["batch_size"]
    is_replace = kwargs["is_replace"]
    table_name = f"{service}_tripdata"
    start_date = datetime(year, 1, 1)
    end_date = datetime(year, 12, 1)
    date_range = list(pd.date_range(start_date, end_date, freq="MS"))
    engine = create_postgres_engine()
    with requests.Session() as session:
        responses = get_files_from_web(service, date_range, session, source)
        response = next(responses)
        export_data_to_postgres(
            service, response, batch_size, table_name, engine, source, is_replace
        )
        for response in get_files_from_web(service, date_range, session, source):
            export_data_to_postgres(
                service, response, batch_size, table_name, engine, source, False
            )
            print(f"Exporting {service} successful")
