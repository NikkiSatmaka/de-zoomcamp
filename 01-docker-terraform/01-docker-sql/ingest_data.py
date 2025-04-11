#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import argparse
from pathlib import Path
from time import time

import niquests
import polars as pl
from sqlalchemy import create_engine


def main(params):
    user = params.user
    password = params.password
    host = params.host
    port = params.port
    db = params.db
    table_name = params.table_name
    url = params.url
    csv_name = "output" + "".join(Path(url).suffixes)

    r = niquests.get(url)
    with open(csv_name, "wb") as f:
        assert r.content is not None
        f.write(r.content)

    engine = create_engine(f"postgresql://{user}:{password}@{host}:{port}/{db}")

    lf = pl.scan_csv(csv_name, try_parse_dates=True)
    n_records = lf.select(pl.len()).collect().item()

    lf.head(n=0).collect().write_database(
        table_name=table_name,
        connection=engine,
        if_table_exists="replace",
        engine="sqlalchemy",
    )

    batch_size = 10_000
    for i in range(0, n_records, batch_size):
        t_start = time()

        lf.slice(i, i + batch_size).collect().write_database(
            table_name="yellow_taxi_data",
            connection=engine,
            engine="sqlalchemy",
            if_table_exists="append",
        )

        t_end = time()

        print(f"inserted another chunk, took {t_end - t_start:.3f} seconds")
    print("finished all iteration")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Ingest CSV data to Postgres")

    parser.add_argument("--user", help="username for postgres")
    parser.add_argument("--password", help="password for postgres")
    parser.add_argument("--host", help="host for postgres")
    parser.add_argument("--port", help="port for postgres")
    parser.add_argument("--db", help="database name for postgres")
    parser.add_argument(
        "--table_name", help="name of the table where we will write the results to"
    )
    parser.add_argument("--url", help="url of the csv file")

    args = parser.parse_args()

    main(args)
