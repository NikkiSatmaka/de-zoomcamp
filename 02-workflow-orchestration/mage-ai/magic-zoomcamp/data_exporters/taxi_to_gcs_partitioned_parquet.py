import os

import pyarrow as pa
import pyarrow.parquet as pq

if "data_exporter" not in globals():
    from mage_ai.data_preparation.decorators import data_exporter


os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "/home/src/google_credentials.json"
bucket_name = 'de-zoomcamp-411717-terra-bucket'
project_id = 'de-zoomcamp-411717'

table_name = "nyc_taxi_data"

root_path = f"{bucket_name}/{table_name}"


@data_exporter
def export_data(data, *args, **kwargs):
    data["tpep_pickup_date"] = data["tpep_pickup_datetime"].dt.date

    table = pa.Table.from_pandas(data)

    gcs = pa.fs.GcsFileSystem()

    pq.write_to_dataset(
        table,
        root_path=root_path,
        partition_cols=["tpep_pickup_date"],
        filesystem=gcs,
    )
