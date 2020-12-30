# -*- coding: utf-8 -*-
import openaq
from datetime import date
import time

MAX_RETRIES = 10


def retrieve_station_measurements(api, station_name, parameter, dt_begin, dt_end):

    print(
        f"""location={station_name},
    parameter={parameter},
    date_from={dt_begin},
    date_to={dt_end},
    limit=10000,
    df=True,
    index="utc",
    order_by="date",
    sort="asc" """
    )

    res1 = None

    for ii in range(1, MAX_RETRIES + 1):

        print(f"{ii} attempt")

        try:
            res1 = api.measurements(
                location=station_name,
                parameter=parameter,
                date_from=dt_begin,
                date_to=dt_end,
                limit=10000,
                df=True,
                index="utc",
                order_by="date",
                sort="asc",
            )
        except openaq.exceptions.ApiError:
            time.sleep(5)
            continue
        else:
            break

    return res1


def main():
    api = openaq.OpenAQ()

    station_name = "US Diplomatic Post: Abu Dhabi"
    parameter = "pm25"
    dt_begin = date(2020, 3, 1)
    dt_end = date(2020, 9, 1)

    res2 = retrieve_station_measurements(api, station_name, parameter, dt_begin, dt_end)

    return res2


if __name__ == "__main__":
    main()

"""

station_name = "US Diplomatic Post: Abu Dhabi"
parameter = "pm25"
dt_begin = date(2019, 3, 1)
dt_end = date(2019, 9, 1)

### >>> a = api.measurements(location=location, parameter=parameter, date_from=date(2018, 1, 1), date_to=date(2018, 10, 1), df=True, index="utc", order_by="date.utc", sort="asc")

"""
