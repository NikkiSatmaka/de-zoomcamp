CREATE DATABASE kestra;
CREATE USER kestra WITH PASSWORD 'k3str4';
GRANT ALL PRIVILEGES ON DATABASE kestra TO kestra;

\c kestra
GRANT ALL PRIVILEGES ON SCHEMA public TO kestra;

\c postgres
