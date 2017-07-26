
This example reuses [activity](../README.md) script for generating user activities in format
suitable for cohort analysis.

## Generating dataset

    ../activity/generate.py -d -c > data.tsv

## Running the ViyaDB

To run the database instance on this dataset, issue the following command when standing in the build/ directory:

    ./src/server/viyad store.json

## Loading the data

First, correct full path to .tsv file in `load.json`.

Then, run:

    curl -sS --data-binary @load.json http://localhost:5000/load

## Sending a query

    curl -sS --data-binary @query.json http://localhost:5000/query

