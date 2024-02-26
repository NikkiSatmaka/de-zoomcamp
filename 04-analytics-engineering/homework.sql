SELECT count(1) FROM `de-zoomcamp-411717.nytaxi.fact_fhv_trips`;

SELECT service_type, count(1) FROM `de-zoomcamp-411717.nytaxi.fact_trips`
WHERE pickup_datetime between '2019-07-01' and '2019-07-31'
GROUP BY service_type;

SELECT count(1) FROM `de-zoomcamp-411717.nytaxi.fact_fhv_trips`
WHERE pickup_datetime between '2019-07-01' and '2019-07-31';
