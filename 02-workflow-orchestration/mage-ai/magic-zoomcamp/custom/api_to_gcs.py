import os
from datetime import datetime
from pathlib import Path
from urllib.parse import urljoin

import pandas as pd
import requests
from google.cloud import storage

if "custom" not in globals():
    from mage_ai.data_preparation.decorators import custom
if "test" not in globals():
    from mage_ai.data_preparation.decorators import test

BUCKET = os.getenv("GCS_BUCKET_NAME")


def get_file_from_api(service, date, session):
    base_url = "https://d37ci6vzurychx.cloudfront.net/trip-data/"
    url_fpath = f'{service}_tripdata_{date.strftime("%Y-%m")}.parquet'
    url = urljoin(base_url, url_fpath)
    return session.get(url)


def upload_to_gcs(bucket, object_key, response_object):
    storage_client = storage.Client()
    bucket = storage_client.bucket(bucket)
    blob = bucket.blob(object_key)
    blob.upload_from_string(
        data=response_object.content,
        content_type=response_object.headers.get("Content-Type", None),
    )


@custom
def web_to_gcs(*args, **kwargs):
    """
    args: The output from any upstream parent blocks (if applicable)

    Returns:
        Anything (e.g. data frame, dictionary, array, int, str, etc.)
    """
    # Specify your custom logic here
    service = kwargs['service']
    year = kwargs['year']
    start_date = datetime(year, 1, 1)
    end_date = datetime(year, 12, 1)
    date_range = list(pd.date_range(start_date, end_date, freq="MS"))
    with requests.Session() as session:
        for date in date_range:
            response = get_file_from_api(service, date, session)
            object_key = Path(response.url).name
            upload_to_gcs(BUCKET, object_key, response)
            print(f"Uploading {object_key} successful")
