#!/bin/bash

curl -sS ftp://ita.ee.lbl.gov/traces/NASA_access_log_Jul95.gz | \
  gunzip - | \
  ./parse.py > data.tsv
