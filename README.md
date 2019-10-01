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

## Data 

The data for this project can be found in the following locations:

- https://www.cms.gov/Research-Statistics-Data-and-Systems/Statistics-Trends-and-Reports/Medicare-Provider-Charge-Data/Part-D-Prescriber.html
- https://www.cms.gov/Research-Statistics-Data-and-Systems/Statistics-Trends-and-Reports/Medicare-Provider-Charge-Data/PartD2017.html
