
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

    curl -sS --data-binary @load.json http://localhost:5000/load

## Sending a query

    curl -sS --data-binary @query.json http://localhost:5000/query

## Stress Testing

Install `siege` if it's not installed yet (shame on you).

Generate sample queries:

    ./queries.py > urls.txt

Run for the first time just to make sure all queries are compiled:

    siege -c 10 -t 3M -f urls.txt -H 'Content-Type: application/json'

Perform the testing by running the same command again:

    siege -c 10 -t 3M -f urls.txt -H 'Content-Type: application/json'

