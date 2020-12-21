# -*- coding: utf-8 -*-
"""
Created on Tue Dec  8 12:13:31 2020

@author: wegia
"""

import openaq
from datetime import date


def retrieve_station_measurements(api, station_name, parameter, dt_begin, dt_end):

    #     print(
    #         f"""location={station_name},
    # parameter={parameter},
    # date_from={dt_begin},
    # date_to={dt_end},
    # limit=10000,
    # df=True,
    # index="utc",
    # order_by="date",
    # sort="asc" """
    #     )

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
    return res1


### >>> a = api.measurements(location=location, parameter=parameter, date_from=date(2018, 1, 1), date_to=date(2018, 10, 1), df=True, index="utc", order_by="date.utc", sort="asc")


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

"""
