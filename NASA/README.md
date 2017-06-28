
This example loads NASA Website access log into ViyaDB.

## Downloading NASA dataset

    ./download.sh

## Running the ViyaDB

To run the database instance on this dataset, issue the following command when standing in the build/ directory:

    ./src/server/viyad ../samples/NASA/store.json

## Loading the data

First, update full path to the .tsv file in `load.json` file.

Then, run:

    curl -sS --data-binary @load.json http://localhost:52341/load

## Sending a query

    curl -sS --data-binary @query.json http://localhost:52341/query

