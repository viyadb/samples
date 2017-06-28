
This example loads simulated activity of mobile users. Such activity includes:

 * clicks
 * impressions
 * installs
 * in-app events
 * launches
 * uninstalls

## Prerequisites

 * [Faker](https://faker.readthedocs.io/en/master/)

## Generating dataset

    ./generate.py > data.tsv

## Running the ViyaDB

To run the database instance on this dataset, issue the following command when standing in the build/ directory:

    ./src/server/viyad store.json

## Loading the data

First, update full path to the .tsv file in `load.json` file.

Then, run:

    curl -sS --data-binary @load.json http://localhost:52341/load

## Sending a query

    curl -sS --data-binary @query.json http://localhost:52341/query

