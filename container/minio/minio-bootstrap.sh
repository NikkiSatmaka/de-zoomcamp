#!/usr/bin/env sh
# shellcheck shell=bash
# shellcheck disable=SC1090

set -euo pipefail

mc alias set --quiet minio http://minio:9000 "$MINIO_ROOT_USER" "$MINIO_ROOT_PASSWORD";
mc admin user add minio "$MINIO_USER" "$MINIO_PASSWORD";
mc admin policy attach minio readwrite --user "$MINIO_USER";

mc admin accesskey create --quiet minio \
    "$MINIO_USER" \
    --name devaccesskey \
    --access-key "$AWS_ACCESS_KEY_ID"  \
    --secret-key  "$AWS_SECRET_ACCESS_KEY";

mc alias set --quiet minio http://minio:9000 "$AWS_ACCESS_KEY_ID" "$AWS_SECRET_ACCESS_KEY";

mc mb --ignore-existing --region "$AWS_REGION" minio/datalake;
mc mb --ignore-existing --region "$AWS_REGION" minio/warehouse;
mc mb --ignore-existing --region "$AWS_REGION" minio/iceberg;
