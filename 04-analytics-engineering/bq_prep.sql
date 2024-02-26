-- Creating external table referring to gcs path
CREATE OR REPLACE EXTERNAL TABLE `de-zoomcamp-411717.nytaxi.external_yellow_tripdata`
OPTIONS (
  format = 'PARQUET',
  uris = ['gs://de-zoomcamp-411717-nytaxi-bucket/yellow/*.parquet']
);

-- Creating external table referring to gcs path
CREATE OR REPLACE EXTERNAL TABLE `de-zoomcamp-411717.nytaxi.external_green_tripdata`
OPTIONS (
  format = 'PARQUET',
  uris = ['gs://de-zoomcamp-411717-nytaxi-bucket/green/*.parquet']
);

-- Creating external table referring to gcs path
CREATE OR REPLACE EXTERNAL TABLE `de-zoomcamp-411717.nytaxi.external_fhv_tripdata`
OPTIONS (
  format = 'PARQUET',
  uris = ['gs://de-zoomcamp-411717-nytaxi-bucket/fhv/*.parquet']
);

CREATE OR REPLACE TABLE `de-zoomcamp-411717.nytaxi.yellow_tripdata` AS
SELECT * FROM `de-zoomcamp-411717.nytaxi.external_yellow_tripdata`;

CREATE OR REPLACE TABLE `de-zoomcamp-411717.nytaxi.green_tripdata` AS
SELECT * FROM `de-zoomcamp-411717.nytaxi.external_green_tripdata`;

CREATE OR REPLACE TABLE `de-zoomcamp-411717.nytaxi.fhv_tripdata` AS
SELECT * FROM `de-zoomcamp-411717.nytaxi.external_fhv_tripdata`;
