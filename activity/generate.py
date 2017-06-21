#!/usr/bin/env python2.7

import codecs
import os
from faker import Faker
from faker.providers import BaseProvider, address, internet, currency
from datetime import datetime, timedelta
from optparse import OptionParser
from time import mktime, time
from hashlib import md5

fake = Faker()
fake.seed(time())

class AppIdProvider(BaseProvider):
  def __init__(self, generator):
    super(AppIdProvider, self).__init__(generator)
    with codecs.open(
        os.path.join(os.path.dirname(os.path.realpath(__file__)), "apps.txt"), encoding="utf-8") as f:
      self.apps = f.read().splitlines()

  def app_id(self):
    r = fake.random.random()
    if r < 0.2:
      return self.random_element(self.apps[0:10])
    if r < 0.4:
      return self.random_element(self.apps[10:100])
    return self.random_element(self.apps)

class InstallDateProvider(BaseProvider):
  def __init__(self, generator):
    super(InstallDateProvider, self).__init__(generator)
    self.current_date = datetime(2015, 01, 01)
    self.events_per_day = 100000
    self.event_counter = 0

  def event_date(self):
    return self.current_date

  def install_date(self):
    self.event_counter += 1
    if self.event_counter % self.events_per_day == 0:
      self.current_date += timedelta(days=1)
    r = fake.random.random()
    if r < 0.4:
      return self.current_date
    if r < 0.70:
      return fake.date_time_between_dates(self.current_date - timedelta(days=5), self.current_date)
    if r < 0.75:
      return fake.date_time_between_dates(self.current_date - timedelta(days=7), self.current_date)
    if r < 0.8:
      return fake.date_time_between_dates(self.current_date - timedelta(days=30), self.current_date)
    return fake.date_time_between_dates(self.current_date - timedelta(days=730), self.current_date)

class AdNetworkProvider(BaseProvider):
  def __init__(self, generator):
    super(AdNetworkProvider, self).__init__(generator)
    with codecs.open(
      os.path.join(os.path.dirname(os.path.realpath(__file__)), "networks.txt"), encoding="utf-8") as f:
      self.networks = f.read().splitlines()

  def ad_network(self):
    r = fake.random.random()
    if r < 0.2:
      return "facebook"
    if r < 0.4:
      return self.random_element(self.networks[0:50])
    return self.random_element(self.networks)

fake.add_provider(address.Provider)
fake.add_provider(currency.Provider)
fake.add_provider(AppIdProvider)
fake.add_provider(InstallDateProvider)
fake.add_provider(AdNetworkProvider)

def random_value(key, prefix, stats):
  r = fake.random.random()
  for s in stats:
    if r < s[0]:
      if s[1] == "":
        return ""
      return "%s%s_%d" % (prefix, key, fake.random_int(1, s[1]))

def hash_vals(*args):
  key = md5()
  key.update("".join(list(args)).encode("utf-8"))
  return key.hexdigest()[0:16]

def generate_events(num_events, cohort, day_granularity):
  for i in range(num_events):
    app_id = fake.app_id()

    install_date = fake.install_date()
    if cohort:
      event_date = fake.event_date()
      days_from_install = str((event_date - install_date).days)
    if day_granularity:
      install_date = install_date.date()
    install_date = install_date.strftime("%s")

    ad_network = fake.ad_network()
    install_country = fake.country_code()
    install_currency = fake.currency_code()
    event_country = install_country if fake.random.random() < 0.9 else fake.country_code()
    event_currency = install_currency if fake.random.random() < 0.9 else fake.currency_code()

    adnet_key = hash_vals(app_id, install_date, ad_network)
    appday_key = hash_vals(app_id, install_date)
    app_key = hash_vals(app_id)

    campaign = random_value(adnet_key, "campaign_", [[0.2, 50], [0.5, 20], [1, 5]])
    campaign_id = campaign.split("_")[1]
    siteid = random_value(adnet_key, "site_", [[0.05, 30000], [0.1, 5000], [0.3, ""], [1, 500]])
    adset = random_value(adnet_key, "", [[0.01, 30], [0.5, ""], [1, 10]])
    adset_id = adset.split("_")[-1]
    adgroup = random_value(adnet_key, "", [[0.01, 30], [0.5, ""], [1, 10]])
    adgroup_id = adgroup.split("_")[-1]
    event_name = random_value(app_key, "event_", [[0.05, 1000], [0.1, 500], [0.5, 100], [1, 5]])
    if cohort:
      user_id = str(int(
          hash_vals(random_value(app_key, "", [[0.05, 10000000], [0.2, 1000000], [0.4, 10000], [0.7, 1000], [1, 200]])),
          16))
    
    r = fake.random.random()
    if r < 0.05: # install
      install_cost = "%.3f" % (20.0/fake.random_int(10, 30))
      install_cost_alt = "%.3f" % (20.0/fake.random_int(10, 30))
      revenue = "0"
      revenue_alt = "0.0"
      installs_count = str(fake.random_int(1, 20))
      launches_count = "0"
      inapps_count = "0"
      clicks_count = "0"
      impressions_count = "0"
      uninstalls_count = "0"
    elif r < 0.056: # uninstalls
      install_cost = "0.0"
      install_cost_alt = "0.0"
      revenue = "0"
      revenue_alt = "0.0"
      installs_count = "0"
      launches_count = "0"
      inapps_count = "0"
      clicks_count = "0"
      impressions_count = "0"
      uninstalls_count = str(fake.random_int(1, 5))
    elif r < 0.15: # clicks
      install_cost = "0.0"
      install_cost_alt = "0.0"
      revenue = "0"
      revenue_alt = "0.0"
      installs_count = "0"
      launches_count = "0"
      inapps_count = "0"
      clicks_count = str(fake.random_int(1, 50))
      impressions_count = "0"
      uninstalls_count = "0"
    elif r < 0.3: # impressions
      install_cost = "0.0"
      install_cost_alt = "0.0"
      revenue = "0"
      revenue_alt = "0.0"
      installs_count = "0"
      launches_count = "0"
      inapps_count = "0"
      clicks_count = "0"
      impressions_count = str(fake.random_int(1, 50))
      uninstalls_count = "0"
    elif r < 0.6: # in-app event
      install_cost = "0.0"
      install_cost_alt = "0.0"
      revenue = "%.3f" % (100.0/fake.random_int(1, 5000))
      revenue_alt = "%.3f" % (100.0/fake.random_int(1, 5000))
      installs_count = "0"
      launches_count = "0"
      inapps_count = str(fake.random_int(1, 50))
      clicks_count = "0"
      impressions_count = "0"
      uninstalls_count = "0"
    else: # launch
      install_cost = "0.0"
      install_cost_alt = "0.0"
      revenue = "0"
      revenue_alt = "0.0"
      installs_count = "0"
      launches_count = str(fake.random_int(1, 50))
      inapps_count = "0"
      clicks_count = "0"
      impressions_count = "0"
      uninstalls_count = "0"

    dims = [
      app_id,
      install_date,
      install_country,
      install_currency,
      ad_network,
      campaign,
      campaign_id,
      siteid,
      adset,
      adset_id,
      adgroup,
      adgroup_id,
      event_country,
      event_currency,
      event_name
    ]
    if cohort:
      dims.append(days_from_install)

    metrics = [
      install_cost,
      install_cost_alt,
      revenue,
      revenue_alt,
      clicks_count,
      impressions_count,
      installs_count,
      launches_count,
      inapps_count,
      uninstalls_count
    ]
    if cohort:
      metrics.insert(0, user_id)

    print("\t".join([s.encode("utf-8") for s in dims + metrics]))

if __name__ == '__main__':
  parser = OptionParser(usage="usage: %prog [options]", version="%prog 1.0")
  parser.add_option("-c", "--cohort",
      action="store_true",
      dest="cohort",
      default=False,
      help="Generate columns needed for calculating cohort")
  parser.add_option("-n", "--number",
      dest="num_events",
      type="int",
      default=10000000,
      help="Number of events to generate")
  parser.add_option("-d", "--day-granularity",
      action="store_true",
      dest="day_granularity",
      default=False,
      help="Whether to generate day granularity events")

  (options, args) = parser.parse_args()
  if len(args) != 0:
    parser.error("wrong number of arguments")

  generate_events(options.num_events, options.cohort, options.day_granularity)

