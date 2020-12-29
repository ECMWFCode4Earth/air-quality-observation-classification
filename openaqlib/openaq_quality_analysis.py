from datetime import datetime
import json
import time
import openaq

from openaq_tools import retrieve_station_measurements
from pecos_tools import (
    run_pecos_tests,
    create_pecos_dashboard,
    generate_dashboard_cell,
)


ROOTDIR = "/Users/miha/git/esowc/air-quality-observation-classification"
ETCDIR = f"{ROOTDIR}/etc"
RESULTSPATH = f"{ROOTDIR}/results"

f = open(f"{ETCDIR}/all_openaq_locations.json")
locations = json.loads(f.read())
N = len(locations)

api = openaq.OpenAQ()

DASHBOARDPATH = f"{RESULTSPATH}/openaq_dashboard.html"
dashboard_content = {}  # Initialize the dashboard content dictionary
location_list = []
parameter_list = []

for nr in range(10):
    # nr = randrange(N)

    location = locations[nr]["location"]
    location_list.append(location)
    start_dt = datetime.strptime(locations[nr]["firstUpdated"], "%Y-%m-%dT%H:%M:%S.%fZ")
    end_dt = datetime.strptime(locations[nr]["lastUpdated"], "%Y-%m-%dT%H:%M:%S.%fZ")
    start_dt = datetime(2020, 12, 1)

    if start_dt < end_dt:
        for parameter in locations[nr]["parameters"][:]:

            print(nr, location, parameter)

            data = retrieve_station_measurements(
                api, location, parameter, start_dt, end_dt
            )
            print(data.head())
            (DA, QCI) = run_pecos_tests(data, location, parameter)
            # print(parameter, data.head(), DA, QCI)
            dashboard_cell = generate_dashboard_cell(DA, QCI)
            dashboard_content[(location, parameter)] = dashboard_cell

            if parameter not in parameter_list:
                parameter_list.append(parameter)
            if location not in location_list:
                location_list.append(location)

            time.sleep(10)

create_pecos_dashboard(parameter_list, location_list, dashboard_content, DASHBOARDPATH)
