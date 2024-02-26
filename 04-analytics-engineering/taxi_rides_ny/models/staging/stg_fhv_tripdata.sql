{{
    config(
        materialized='view'
    )
}}

with tripdata as 
(
    select
        -- identifiers
        dispatching_base_num,
        {{ dbt.safe_cast("pulocationid", api.Column.translate_type("integer")) }} as pickup_locationid,
        {{ dbt.safe_cast("dolocationid", api.Column.translate_type("integer")) }} as dropoff_locationid,
        
        -- timestamps
        timestamp_millis(cast(pickup_datetime / 1000000 as int64)) as pickup_datetime,
        timestamp_millis(cast(dropoff_datetime / 1000000 as int64)) as dropoff_datetime,   
        
        -- trip info
        sr_flag,
        affiliated_base_number
  from {{ source('staging','fhv_tripdata') }}
)
select *
from tripdata
where extract(year from pickup_datetime) = 2019

-- dbt build --select <model_name> --vars '{'is_test_run': 'false'}'
{% if var('is_test_run', default=true) %}

  limit 100

{% endif %}
