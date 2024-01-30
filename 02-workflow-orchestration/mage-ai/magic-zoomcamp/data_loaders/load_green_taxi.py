import io
from datetime import datetime
from urllib.parse import urljoin
import pandas as pd
import requests
if "data_loader" not in globals():
    from mage_ai.data_preparation.decorators import data_loader
if "test" not in globals():
    from mage_ai.data_preparation.decorators import test


@data_loader
def load_data_from_api(*args, **kwargs):
    """
    Template for loading data from API
    """
    start_date = datetime(2020, 10, 1)
    end_date = datetime(2020, 12, 1)
    date_range = list(pd.date_range(start_date, end_date, freq='MS'))
    base_url = "https://github.com/DataTalksClub/nyc-tlc-data/releases/download/green/"
    
    taxi_dtypes = {
        "VendorID": "float64",
        "store_and_fwd_flag": "object",
        "RatecodeID": "float64",
        "PULocationID": "int64",
        "DOLocationID": "int64",
        "passenger_count": "float64",
        "trip_distance": "float64",
        "fare_amount": "float64",
        "extra": "float64",
        "mta_tax": "float64",
        "tip_amount": "float64",
        "tolls_amount": "float64",
        "ehail_fee": "float64",
        "improvement_surcharge": "float64",
        "total_amount": "float64",
        "payment_type": "float64",
        "trip_type": "float64",
        "congestion_surcharge": "float64",
    }

    parse_dates = ["lpep_pickup_datetime", "lpep_dropoff_datetime"]

    df_taxi = []
    for date in date_range:
        url_fpath = f'green_tripdata_{date.strftime("%Y-%m")}.csv.gz'
        url = urljoin(base_url, url_fpath)
        df_taxi.append(pd.read_csv(url, sep=",", compression="gzip", dtype=taxi_dtypes, parse_dates=parse_dates))
        
    return pd.concat(df_taxi)


@test
def test_output(output, *args) -> None:
    """
    Template code for testing the output of the block.
    """
    assert output is not None, "The output is undefined"
