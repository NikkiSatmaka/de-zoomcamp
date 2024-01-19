## Module 1 Homework

## Docker & SQL

In this homework we'll prepare the environment
and practice with Docker and SQL


## Question 1. Knowing docker tags

Run the command to get information on Docker

```docker run --help```

Which tag has the following text? - *Automatically remove the container when it exits*

- `--rm`


## Question 2. Understanding docker first run

Run docker with the python:3.9 image in an interactive mode and the entrypoint of bash.
Now check the python modules that are installed ( use ```pip list``` ).

```docker run -it --rm python:3.9 bash```

What is version of the package *wheel* ?

- 0.42.0


# Prepare Postgres

Run Postgres and load data as shown in the videos
We'll use the green taxi trips from September 2019:

```wget https://github.com/DataTalksClub/nyc-tlc-data/releases/download/green/green_tripdata_2019-09.csv.gz```

You will also need the dataset with zones:

```wget https://s3.amazonaws.com/nyc-tlc/misc/taxi+_zone_lookup.csv```

Download this data and put it into Postgres (with jupyter notebooks or with a pipeline)

```bash
docker run -it --rm \
  --network=01-docker-sql_default \
  taxi_ingest:v001 \
  --user=root \
  --password=root \
  --host=pgdatabase \
  --port=5432 \
  --db=ny_taxi \
  --table_name=green_taxi_trips \
  --url=https://github.com/DataTalksClub/nyc-tlc-data/releases/download/green/green_tripdata_2019-09.csv.gz
```


## Question 3. Count records

How many taxi trips were totally made on September 18th 2019?

```sql
select
	count(1)
from green_taxi_trips
where lpep_pickup_datetime >= '2019-09-18' and lpep_pickup_datetime < '2019-09-19'
and lpep_dropoff_datetime >= '2019-09-18' and lpep_dropoff_datetime < '2019-09-19';
```

Tip: started and finished on 2019-09-18.

Remember that `lpep_pickup_datetime` and `lpep_dropoff_datetime` columns are in the format timestamp (date and hour+min+sec) and not in date.

- 15612

## Question 4. Largest trip for each day

Which was the pick up day with the largest trip distance
Use the pick up time for your calculations.

```sql
select date_trunc('day', lpep_pickup_datetime)
from green_taxi_trips
where trip_distance = (
	select max(trip_distance)
	from green_taxi_trips
);
```

- 2019-09-26


## Question 5. Three biggest pick up Boroughs

Consider lpep_pickup_datetime in '2019-09-18' and ignoring Borough has Unknown

Which were the 3 pick up Boroughs that had a sum of total_amount superior to 50000?

```sql
select
	z."Borough",
	sum(g.total_amount) total_amount
from green_taxi_trips g
join zones z
on g."PULocationID" = z."LocationID"
where g.lpep_pickup_datetime >= '2019-09-18' and g.lpep_pickup_datetime < '2019-09-19'
group by z."Borough"
having sum(g.total_amount) > 50000
order by total_amount desc;
```

- "Brooklyn" "Manhattan" "Queens"


## Question 6. Largest tip

For the passengers picked up in September 2019 in the zone name Astoria which was the drop off zone that had the largest tip?
We want the name of the zone, not the id.

```sql
select
	zpu."Zone" "PUZone",
	zdo."Zone" "DOZone",
	g.tip_amount
from green_taxi_trips g
join zones zpu
on g."PULocationID" = zpu."LocationID"
join zones zdo
on g."DOLocationID" = zdo."LocationID"
where g.lpep_pickup_datetime >= '2019-09-01' and g.lpep_pickup_datetime < '2019-10-01'
and zpu."Zone" = 'Astoria'
order by tip_amount desc
limit 1;

```

Note: it's not a typo, it's `tip` , not `trip`

- JFK Airport



## Terraform

In this section homework we'll prepare the environment by creating resources in GCP with Terraform.

In your VM on GCP/Laptop/GitHub Codespace install Terraform.
Copy the files from the course repo
[here](https://github.com/DataTalksClub/data-engineering-zoomcamp/tree/main/01-docker-terraform/1_terraform_gcp/terraform) to your VM/Laptop/GitHub Codespace.

Modify the files as necessary to create a GCP Bucket and Big Query Dataset.


## Question 7. Creating Resources

After updating the main.tf and variable.tf files run:

```
terraform apply
```

Paste the output of this command into the homework submission form.

## Submitting the solutions

* Form for submitting: https://courses.datatalks.club/de-zoomcamp-2024/homework/hw01
* You can submit your homework multiple times. In this case, only the last submission will be used.

Deadline: 29 January, 23:00 CET
