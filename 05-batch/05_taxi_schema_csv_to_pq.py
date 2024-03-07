#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from pathlib import Path

from pyspark.sql import SparkSession
from schemas import taxi_schema

spark = SparkSession.builder.master("local[*]").appName("test").getOrCreate()

services = ["yellow", "green", "fhv", "fhvhv"]
for service in services:
    for input_path in Path(f"data/raw/{service}").rglob("*.csv.gz"):
        output_path = Path("data/pq") / input_path.parent.relative_to("data/raw")
        output_path.parent.mkdir(parents=True, exist_ok=True)

        schema = taxi_schema[service]
        if service == "fhvhv" and "2021-06" in input_path.name:
            schema = taxi_schema["fhv"]

        df = (
            spark.read.option("header", "true")
            .schema(schema)
            .csv(str(input_path.parent))
        )

        df.repartition(4).write.parquet(str(output_path))

spark.sparkContext.stop()
spark.stop()
