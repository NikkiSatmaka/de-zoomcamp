-- Creating external table referring to gcs path
CREATE OR REPLACE EXTERNAL TABLE `de-zoomcamp-411717.nytaxi.external_green_tripdata`
OPTIONS (
  format = 'PARQUET',
  uris = ['gs://de-zoomcamp-411717-nytaxi-bucket/green_tripdata_2022-*.parquet']
);

SELECT COUNT(1) FROM `de-zoomcamp-411717.nytaxi.external_green_tripdata`;

-- Create a non partitioned table from external table
CREATE OR REPLACE TABLE `de-zoomcamp-411717.nytaxi.green_tripdata_non_partitioned` AS
SELECT * FROM `de-zoomcamp-411717.nytaxi.external_green_tripdata`;

-- Create a partitioned table from external table
CREATE OR REPLACE TABLE `de-zoomcamp-411717.nytaxi.green_tripdata_partitioned`
PARTITION BY
  DATE(`lpep_pickup_datetime`) AS
SELECT * FROM `de-zoomcamp-411717.nytaxi.external_green_tripdata`;

-- Query scans 0 B
SELECT DISTINCT `PULocationID`
FROM `de-zoomcamp-411717.nytaxi.external_green_tripdata`;

-- Query scans 6.41 MB
SELECT DISTINCT `PULocationID`
FROM `de-zoomcamp-411717.nytaxi.green_tripdata_non_partitioned`;

-- Query scans 6.41 MB
SELECT DISTINCT `PULocationID`
FROM `de-zoomcamp-411717.nytaxi.green_tripdata_partitioned`;

SELECT COUNT(1)
FROM `de-zoomcamp-411717.nytaxi.green_tripdata_non_partitioned`
WHERE `fare_amount` = 0;

-- Create a partitioned and clustered table from external table
CREATE OR REPLACE TABLE `de-zoomcamp-411717.nytaxi.green_tripdata_partitioned_clustered`
PARTITION BY
  DATE(`lpep_pickup_datetime`)
CLUSTER BY
  `PULocationID` AS
SELECT * FROM `de-zoomcamp-411717.nytaxi.external_green_tripdata`;

-- Check the partitions available
SELECT table_name, partition_id, total_rows
FROM `de-zoomcamp-411717.nytaxi.INFORMATION_SCHEMA.PARTITIONS`
ORDER BY table_name, partition_id;

-- Write a query to retrieve the distinct PULocationID between lpep_pickup_datetime 06/01/2022 and 06/30/2022 (inclusive)
-- Query scans 12.82 MB
SELECT DISTINCT `PULocationID`
FROM `de-zoomcamp-411717.nytaxi.green_tripdata_non_partitioned`
WHERE `lpep_pickup_datetime` BETWEEN '2022-06-01' AND '2022-06-30';

-- Query scans 1.12 MB
SELECT DISTINCT `PULocationID`
FROM `de-zoomcamp-411717.nytaxi.green_tripdata_partitioned_clustered`
WHERE `lpep_pickup_datetime` BETWEEN '2022-06-01' AND '2022-06-30';

-- Query scans 0 B
SELECT COUNT(*)
FROM `de-zoomcamp-411717.nytaxi.green_tripdata_partitioned_clustered`;

-- Query scans 0 B
SELECT COUNT(*)
FROM `de-zoomcamp-411717.nytaxi.green_tripdata_non_partitioned`;
