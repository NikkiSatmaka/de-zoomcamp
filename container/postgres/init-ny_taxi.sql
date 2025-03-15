CREATE DATABASE ny_taxi;
CREATE USER nikki WITH PASSWORD 'password';
GRANT ALL PRIVILEGES ON DATABASE ny_taxi TO nikki;

\c ny_taxi
GRANT ALL PRIVILEGES ON SCHEMA public TO nikki;

\c postgres
