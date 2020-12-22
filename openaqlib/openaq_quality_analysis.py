from datetime import datetime
import json
from random import randrange
import pprint

import openaq
import pecos

from openaq_tools import retrieve_station_measurements

ETCDIR = "/home/mo/mod/git/esowc/code_2020/air-quality-observation-classification/etc"

f = open(f"{ETCDIR}/all_openaq_locations.json")
locations = json.loads(f.read())

N = len(locations)


for ii in range(5):
    nr = randrange(N)
    api = openaq.OpenAQ()

    # pprint.pprint(locations[nr])
    print()

    location = locations[nr]["location"]
    start_dt = datetime.strptime(locations[nr]["firstUpdated"], "%Y-%m-%dT%H:%M:%S.%fZ")
    end_dt = datetime.strptime(locations[nr]["lastUpdated"], "%Y-%m-%dT%H:%M:%S.%fZ")
    start_dt = datetime(2020, 12, 1)

    if start_dt < end_dt:
        for parameter in locations[nr]["parameters"]:
            data = retrieve_station_measurements(
                api, location, parameter, start_dt, end_dt
            )
            print(parameter, data.head())
