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

## Data 

The data for this project can be found in the following locations:

- https://www.cms.gov/Research-Statistics-Data-and-Systems/Statistics-Trends-and-Reports/Medicare-Provider-Charge-Data/Part-D-Prescriber.html
- https://www.cms.gov/Research-Statistics-Data-and-Systems/Statistics-Trends-and-Reports/Medicare-Provider-Charge-Data/PartD2017.html
