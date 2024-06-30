#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from pyspark.sql import types as T

taxi_schema = {
    "yellow": T.StructType(
        [
            T.StructField("VendorID", T.IntegerType(), True),
            T.StructField("tpep_pickup_datetime", T.TimestampType(), True),
            T.StructField("tpep_dropoff_datetime", T.TimestampType(), True),
            T.StructField("passenger_count", T.IntegerType(), True),
            T.StructField("trip_distance", T.FloatType(), True),
            T.StructField("RatecodeID", T.IntegerType(), True),
            T.StructField("store_and_fwd_flag", T.StringType(), True),
            T.StructField("PULocationID", T.IntegerType(), True),
            T.StructField("DOLocationID", T.IntegerType(), True),
            T.StructField("payment_type", T.IntegerType(), True),
            T.StructField("fare_amount", T.FloatType(), True),
            T.StructField("extra", T.FloatType(), True),
            T.StructField("mta_tax", T.FloatType(), True),
            T.StructField("tip_amount", T.FloatType(), True),
            T.StructField("tolls_amount", T.FloatType(), True),
            T.StructField("improvement_surcharge", T.FloatType(), True),
            T.StructField("total_amount", T.FloatType(), True),
            T.StructField("congestion_surcharge", T.FloatType(), True),
        ]
    ),
    "green": T.StructType(
        [
            T.StructField("VendorID", T.IntegerType(), True),
            T.StructField("lpep_pickup_datetime", T.TimestampType(), True),
            T.StructField("lpep_dropoff_datetime", T.TimestampType(), True),
            T.StructField("store_and_fwd_flag", T.StringType(), True),
            T.StructField("RatecodeID", T.IntegerType(), True),
            T.StructField("PULocationID", T.IntegerType(), True),
            T.StructField("DOLocationID", T.IntegerType(), True),
            T.StructField("passenger_count", T.IntegerType(), True),
            T.StructField("trip_distance", T.FloatType(), True),
            T.StructField("fare_amount", T.FloatType(), True),
            T.StructField("extra", T.FloatType(), True),
            T.StructField("mta_tax", T.FloatType(), True),
            T.StructField("tip_amount", T.FloatType(), True),
            T.StructField("tolls_amount", T.FloatType(), True),
            T.StructField("ehail_fee", T.FloatType(), True),
            T.StructField("improvement_surcharge", T.FloatType(), True),
            T.StructField("total_amount", T.FloatType(), True),
            T.StructField("payment_type", T.IntegerType(), True),
            T.StructField("trip_type", T.IntegerType(), True),
            T.StructField("congestion_surcharge", T.FloatType(), True),
        ]
    ),
    "fhv": T.StructType(
        [
            T.StructField("dispatching_base_num", T.StringType(), True),
            T.StructField("pickup_datetime", T.TimestampType(), True),
            T.StructField("dropoff_datetime", T.TimestampType(), True),
            T.StructField("PULocationID", T.IntegerType(), True),
            T.StructField("DOLocationID", T.IntegerType(), True),
            T.StructField("SR_Flag", T.IntegerType(), True),
            T.StructField("Affiliated_base_number", T.StringType(), True),
        ]
    ),
    "fhvhv": T.StructType(
        [
            T.StructField("hvfhs_license_num", T.StringType(), True),
            T.StructField("dispatching_base_num", T.StringType(), True),
            T.StructField("pickup_datetime", T.TimestampType(), True),
            T.StructField("dropoff_datetime", T.TimestampType(), True),
            T.StructField("PULocationID", T.IntegerType(), True),
            T.StructField("DOLocationID", T.IntegerType(), True),
            T.StructField("SR_Flag", T.IntegerType(), True),
        ]
    ),
}
