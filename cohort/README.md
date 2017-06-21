
This example reuses [activity](../README.md) script for generating user activities in format
suitable for cohort analysis.

## Generating dataset

    ../activity/generate.py -d -c > data.tsv

## Running the ViyaDB

To run the database instance on this dataset, issue the following command when standing in the build/ directory:

    ./src/server/viyad ../samples/cohort/store.json

## Loading the data

    curl -sS --data-binary @load.json http://localhost:52341/load

## Sending a query

    curl -sS --data-binary @query.json http://localhost:52341/query

