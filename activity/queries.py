#!/usr/bin/env python2.7

import os
import codecs
import json
import random

with codecs.open(os.path.join(os.path.dirname(os.path.realpath(__file__)), "apps.txt"), encoding="utf-8") as f:
  apps = f.read().splitlines()

with codecs.open(os.path.join(os.path.dirname(os.path.realpath(__file__)), "networks.txt"), encoding="utf-8") as f:
  networks = f.read().splitlines()

dim_groups = [
  ["install_date", "install_country", "ad_network", "campaign"],
  ["install_date", "ad_network", "campaign"],
  ["install_date", "install_country", "ad_network"],
  ["install_date", "ad_network", "campaign", "event_name"],
  ["install_date", "install_country", "ad_network", "campaign", "event_name"]
]

metric_groups = [
  ["installs_count", "clicks_count", "launches_count"],
  ["installs_count", "install_cost", "install_cost_alt", "revenue", "revenue_alt"],
  ["revenue", "revenue_alt", "inapps_count"],
  ["clicks_count", "impressions_count", "installs_count", "launches_count"],
  ["clicks_count", "impressions_count", "installs_count", "uninstalls_count"]
]

date_ranges = [
  ["2015-01-01", "2015-01-14"],
  ["2015-01-01", "2015-01-30"],
  ["2013-05-01", "2013-05-14"],
  ["2014-01-01", "2015-03-01"],
  ["2014-12-01", "2015-01-01"],
  ["2015-02-01", "2015-02-08"],
  ["2013-01-01", "2013-03-01"]
]

country_groups = [
  ["US", "IR", "UK", "MX"],
  ["US", "IL", "KZ"],
  ["RU", "BE"],
  ["TG", "TH", "TJ", "TL", "TM", "TN", "TO", "TR", "TT", "TV", "TZ", "UA", "UG", "US", "UY", "UZ", "VA", "VC", "VE", "VN", "VU", "WS", "YE", "ZA", "ZM", "ZW"]
]

for i in range(1000):
  dates = random.choice(date_ranges)
  query = {
    "type": "aggregate",
    "table": "activity",
    "select": [],
    "filter": {
      "op": "and",
      "filters": [
        {"op": "eq", "column": "app_id", "value": random.choice(apps)},
        {"op": "ge", "column": "install_date", "value": dates[0]},
        {"op": "lt", "column": "install_date", "value": dates[1]}
      ]
    }
  }
  query["select"] = [{"column": c} for c in random.choice(dim_groups) + random.choice(metric_groups)]

  if random.random() < 0.2:
    query["filter"]["filters"].append({"op": "in", "column": "install_country", "values": random.choice(country_groups)})

  if random.random() < 0.5:
    query["filter"]["filters"].append({"op": "eq", "column": "ad_network", "value": random.choice(networks)})
    
  print "http://localhost:52341/query POST %s" % json.dumps(query)

