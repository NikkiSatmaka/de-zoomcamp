import io
import os
from datetime import datetime
from pathlib import Path
from urllib.parse import urljoin

import pandas as pd
import requests
from google.cloud import storage

from magic_zoomcamp.utils.dtypes import taxi_dtypes, taxi_parse_dates

if "custom" not in globals():
    from mage_ai.data_preparation.decorators import custom
if "test" not in globals():
    from mage_ai.data_preparation.decorators import test

BUCKET = os.getenv("GCS_BUCKET_NAME")


def get_file_from_web(service, date, session, source="original"):
    """_summary_

    Args:
        service (_type_): _description_
        date (_type_): _description_
        session (_type_): _description_
        source (str, optional): source of the file. Defaults to "original".

    Returns:
        _type_: _description_
    """
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


def csv_to_parquet(service, response_object_content):
    df = pd.read_csv(
        io.BytesIO(response_object_content),
        dtype=taxi_dtypes[service],
        compression="gzip",
    )
    df[taxi_parse_dates[service]] = df[taxi_parse_dates[service]].apply(pd.to_datetime)
    df.columns = df.columns.str.lower()
    return df.to_parquet()


def upload_to_gcs(service, bucket, object_key, response_object, source="original"):
    data = response_object.content
    if source != "original":
        data = csv_to_parquet(service, data)
    storage_client = storage.Client()
    bucket = storage_client.bucket(bucket)
    blob = bucket.blob(object_key)
    blob.upload_from_string(
        data=data,
        content_type=response_object.headers.get("Content-Type", None),
    )


def obtain_object_key(service, year, response, source):
    if source == "original":
        object_key = f"{service}/{year}/{Path(response.url).name}"
    else:
        object_key = response.headers.get("Content-Disposition")
        if object_key is None:
            return
        object_key = Path(object_key.split("=")[-1])
        while object_key.suffix:
            object_key = object_key.with_suffix("")
        object_key = object_key.with_suffix(".parquet")
        object_key = f"{service}/{year}/{object_key}"
    return object_key


@custom
def web_to_gcs(*args, **kwargs):
    """
    args: The output from any upstream parent blocks (if applicable)

    Returns:
        Anything (e.g. data frame, dictionary, array, int, str, etc.)
    """
    # Specify your custom logic here
    service = kwargs["service"]
    year = kwargs["year"]
    source = kwargs["source"]
    start_date = datetime(year, 1, 1)
    end_date = datetime(year, 12, 1)
    date_range = list(pd.date_range(start_date, end_date, freq="MS"))
    with requests.Session() as session:
        for response in get_files_from_web(service, date_range, session, source):
            object_key = obtain_object_key(service, year, response, source)
            upload_to_gcs(service, BUCKET, object_key, response, source)
            print(f"Uploading {object_key} successful")
