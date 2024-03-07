#!/usr/bin/env bash
# -*- coding: utf-8 -*-

set -e

SERVICE=$1 # yellow
YEAR=$2    # 2019

BASE_URL="https://github.com/DataTalksClub/nyc-tlc-data/releases/download"

for month in {01..12}; do
    url_fname="${SERVICE}_tripdata_${YEAR}-${month}"
    url_fpath="${SERVICE}/${url_fname}.csv.gz"
    url="${BASE_URL}/${url_fpath}"

    local_prefix="data/raw/${SERVICE}/${YEAR}/${month}"
    local_file="${url_fname}.csv.gz"
    local_path="${local_prefix}/${local_file}"

    echo "downloading ${url} to ${local_path}"
    mkdir -p ${local_prefix}
    wget ${url} -O ${local_path}
done
