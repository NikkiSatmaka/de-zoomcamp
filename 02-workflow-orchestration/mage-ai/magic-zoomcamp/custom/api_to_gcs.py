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


def get_file_from_api(*args, **kwargs):
    """
    Template for loading data from API
    """
    session = kwargs.get("session")
    date = kwargs.get("date")

    base_url = "https://d37ci6vzurychx.cloudfront.net/trip-data/"
    url_fpath = f'green_tripdata_{date.strftime("%Y-%m")}.parquet'
    url = urljoin(base_url, url_fpath)

    return session.get(url)


@custom
def upload_to_gcs(*args, **kwargs):
    """
    args: The output from any upstream parent blocks (if applicable)

    Returns:
        Anything (e.g. data frame, dictionary, array, int, str, etc.)
    """
    # Specify your custom logic here
    start_date = datetime(2022, 1, 1)
    end_date = datetime(2022, 12, 1)
    date_range = list(pd.date_range(start_date, end_date, freq="MS"))

    bucket_name = os.getenv("GCS_BUCKET_NAME")

    storage_client = storage.Client()
    bucket = storage_client.bucket(bucket_name)

    with requests.Session() as session:
        for date in date_range:
            response = get_file_from_api(date=date, session=session)
            object_key = Path(response.url).name
            blob = bucket.blob(object_key)

            blob.upload_from_string(
                data=response.content,
                content_type=response.headers.get("Content-Type", None),
            )
            print(f"Uploading {object_key} successful")

    return {}


@test
def test_output(output, *args) -> None:
    """
    Template code for testing the output of the block.
    """
    assert output is not None, "The output is undefined"
