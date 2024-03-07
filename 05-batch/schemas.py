#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from pyspark.sql import types

taxi_schema = {
    "yellow": types.StructType(
        [
            types.StructField("VendorID", types.IntegerType(), True),
            types.StructField("tpep_pickup_datetime", types.TimestampType(), True),
            types.StructField("tpep_dropoff_datetime", types.TimestampType(), True),
            types.StructField("passenger_count", types.IntegerType(), True),
            types.StructField("trip_distance", types.FloatType(), True),
            types.StructField("RatecodeID", types.IntegerType(), True),
            types.StructField("store_and_fwd_flag", types.StringType(), True),
            types.StructField("PULocationID", types.IntegerType(), True),
            types.StructField("DOLocationID", types.IntegerType(), True),
            types.StructField("payment_type", types.IntegerType(), True),
            types.StructField("fare_amount", types.FloatType(), True),
            types.StructField("extra", types.FloatType(), True),
            types.StructField("mta_tax", types.FloatType(), True),
            types.StructField("tip_amount", types.FloatType(), True),
            types.StructField("tolls_amount", types.FloatType(), True),
            types.StructField("improvement_surcharge", types.FloatType(), True),
            types.StructField("total_amount", types.FloatType(), True),
            types.StructField("congestion_surcharge", types.FloatType(), True),
        ]
    ),
    "green": types.StructType(
        [
            types.StructField("VendorID", types.IntegerType(), True),
            types.StructField("lpep_pickup_datetime", types.TimestampType(), True),
            types.StructField("lpep_dropoff_datetime", types.TimestampType(), True),
            types.StructField("store_and_fwd_flag", types.StringType(), True),
            types.StructField("RatecodeID", types.IntegerType(), True),
            types.StructField("PULocationID", types.IntegerType(), True),
            types.StructField("DOLocationID", types.IntegerType(), True),
            types.StructField("passenger_count", types.IntegerType(), True),
            types.StructField("trip_distance", types.FloatType(), True),
            types.StructField("fare_amount", types.FloatType(), True),
            types.StructField("extra", types.FloatType(), True),
            types.StructField("mta_tax", types.FloatType(), True),
            types.StructField("tip_amount", types.FloatType(), True),
            types.StructField("tolls_amount", types.FloatType(), True),
            types.StructField("ehail_fee", types.FloatType(), True),
            types.StructField("improvement_surcharge", types.FloatType(), True),
            types.StructField("total_amount", types.FloatType(), True),
            types.StructField("payment_type", types.IntegerType(), True),
            types.StructField("trip_type", types.IntegerType(), True),
            types.StructField("congestion_surcharge", types.FloatType(), True),
        ]
    ),
    "fhv": types.StructType(
        [
            types.StructField("dispatching_base_num", types.StringType(), True),
            types.StructField("pickup_datetime", types.TimestampType(), True),
            types.StructField("dropoff_datetime", types.TimestampType(), True),
            types.StructField("PULocationID", types.IntegerType(), True),
            types.StructField("DOLocationID", types.IntegerType(), True),
            types.StructField("SR_Flag", types.IntegerType(), True),
            types.StructField("Affiliated_base_number", types.StringType(), True),
        ]
    ),
    "fhvhv": types.StructType(
        [
            types.StructField("hvfhs_license_num", types.StringType(), True),
            types.StructField("dispatching_base_num", types.StringType(), True),
            types.StructField("pickup_datetime", types.TimestampType(), True),
            types.StructField("dropoff_datetime", types.TimestampType(), True),
            types.StructField("PULocationID", types.IntegerType(), True),
            types.StructField("DOLocationID", types.IntegerType(), True),
            types.StructField("SR_Flag", types.IntegerType(), True),
        ]
    ),
}
