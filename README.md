# Fraud Detection Pipeline

This project contains the code for the final project of the Udacity Data Engineering Nano Degree.

## Setting up the project

The project runs on Docker compose.

Requirements:

- Docker

Running the app:

```bash
docker-compose build # only needed when changing airflow dependencies
docker-compose up
```

Airflow is then available on port 8080 on localhost.

## Scope

The goal of the project is to create an ETL pipeline to load in provider payments data + provider prescriptions data in order to determine whether providers where motivated by specific parties to prescribe more of a specific drug. This will be stored in an analytical data warehouse with the aim to provide an easy to use data model to answer questions such as:

- Did providers paid by a specific pharmaceutical company prescribe more drugs
- Is there a specific region in which certain pharmaceutical companies are active
- Which type of providers recieved the most payments

## Choice of tools

Airflow: Airflow provides the scheduling capabilities for the ETL pipeline and ensures data is loaded in the correct order. Airflow ensures that when failure occurs in the ETL pipeline, downstream dependent task are not triggered.
Postgresql: Postgresql serves as the Data Warehouse as it can be run locally. It is not an MPP-database, but given the relativily small size of the datasets (biggest dataset is ±7GB), it serves its purpose. Postgres provides a couple of useful functions such as COPY FROM (CSV/TXT), and due to its plugin based nature can easily be extended to provide MPP like capabilities. It also has extensive data type support. Postgres is also compatible with Redshift, making migration to a more scalable system easier.
Docker: Docker provides the ability to easily bootstrap the project on a local machine. Again, due to the size of the data sets, this should serve its purpose.

## Scaling

In this sections we discuss a set of questions with regards of scaling the ETL pipeline and what effect that would have on the project.

### What if the data was increased by 100x

First of all, the goal if the data increases by 100x would be to move away from a local database. While hard drives of 2 TB are accessible, maintaining a local system at that scale would become hard. A valid possibility would be to move to a managed Postgres database in the cloud (e.g. AWS RDS) and use a single large instance. However, Postgres is not optimized for analytical queries and this would lead to an enormous increase in the time required to load and transform the data. A better approach would be to move to a data warehouse, such as AWS Redshift or Snowflake. Both provide horizontal scaling and easily accessing data from AWS S3. Snowflake however, seperates storage from compute, meaning 2 TB could be stored in S3, while the Data Warehouse only needs to run while it is accessed (for example, only 9-6).

### What if the pipelines would be run on a daily basis by 7 am every day

Due to using Airflow, the scheduling is already taken care of. However, in order to ensure consistent success, a couple of points need to be addressed:

1. Retries: If a task fails due to for example a random network error, it should be configured to retry x amount of times
2. Alerting: If after a certain number of retries it still fails, an alert needs to be sent to the operations team. For example using the on_failure_callback of a task together with the Slack operator
3. Dependencies between dags: The enriched-dag is scheduled after the staging-dag, and should only be run once the staging-dag is complete. Otherwise there is a risk that either no data or incorrect data is added to the enriched scheme. The ExternalTaskSensor could be utilised.

### What if the database needed to be accessed by 100+ people

The answer here is partly similar to the increase in data size. Moving to a cloud based data warehouse is the solution, as more people means an increase in compute power neede. Additional improvements can be made by monitoring the common query patterns and building materialized views/summary tables to provide answers to questions commonly asked. Certain data can already be pre-aggregated in the ETL job, so that these queries require less compute power.  

## Data 

The data for this project can be found in the following locations:

- https://www.cms.gov/Research-Statistics-Data-and-Systems/Statistics-Trends-and-Reports/Medicare-Provider-Charge-Data/Part-D-Prescriber.html
- https://www.cms.gov/Research-Statistics-Data-and-Systems/Statistics-Trends-and-Reports/Medicare-Provider-Charge-Data/PartD2017.html
