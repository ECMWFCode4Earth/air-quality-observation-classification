from datetime import datetime
import json
from random import randrange
import pprint

import openaq
import pecos

from openaq_tools import retrieve_station_measurements
from pecos_tools import (
    run_pecos_tests,
    # generate_pecos_dashboard,
    # generate_dashboard_cell,
)


ETCDIR = "/home/mo/mod/git/esowc/code_2020/air-quality-observation-classification/etc"
RESULTSPATH = "perm/mo/mod/tmp/openaq_results"

f = open(f"{ETCDIR}/all_openaq_locations.json")
locations = json.loads(f.read())
N = len(locations)

api = openaq.OpenAQ()

DASHBOARDPATH = f"{RESULTSPATH}/openaq_dashboard.html"
dashboard_content = {}  # Initialize the dashboard content dictionary
location_list = []
parameter_list = []

for nr in range(1):
    # nr = randrange(N)

    location = locations[nr]["location"]
    location_list.append(location)
    start_dt = datetime.strptime(locations[nr]["firstUpdated"], "%Y-%m-%dT%H:%M:%S.%fZ")
    end_dt = datetime.strptime(locations[nr]["lastUpdated"], "%Y-%m-%dT%H:%M:%S.%fZ")
    start_dt = datetime(2020, 12, 1)

    if start_dt < end_dt:
        for parameter in locations[nr]["parameters"]:
            data = retrieve_station_measurements(
                api, location, parameter, start_dt, end_dt
            )
            print(parameter, data.head())
            test_results = run_pecos_tests(data, location, parameter)
            # dashboard_cell = generate_dashboard_cell()
            # dashboard_content[(location, parameter)] = dashboard_cell

# generate_pecos_dashboard(
#     parameter_list, location_list, dashboard_content, DASHBOARDPATH
# )
