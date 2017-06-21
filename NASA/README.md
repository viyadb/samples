
This example loads NASA Website access log into ViyaDB.

## Downloading NASA dataset

    ./download.sh

## Running the ViyaDB

To run the database instance on this dataset, issue the following command when standing in the build/ directory:

    ./src/server/viyad ../samples/NASA/store.json

## Loading the data

    curl -sS --data-binary @data.tsv http://localhost:52341/tables/access_log/data

## Sending a query

    curl -sS --data-binary @query.json http://localhost:52341/query

