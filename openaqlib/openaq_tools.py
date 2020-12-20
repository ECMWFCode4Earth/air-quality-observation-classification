# -*- coding: utf-8 -*-
"""
Created on Tue Dec  8 12:13:31 2020

@author: wegia
"""

import openaq
from datetime import date


def retrieve_station_measurements(api, station_name, parameter, dt_begin, dt_end):

    res1 = api.measurements(location=station_name,
                            parameter=parameter,
                            date_from=dt_begin,
                            date_to=dt_end,
                            limit=10000,
                            df=True
                            )
    return res1


def main(parameter_list):
    api = openaq.OpenAQ()

    station_name = 'US Diplomatic Post: Abu Dhabi'
    parameter = 'pm25'
    dt_begin = date(2020, 3, 1)
    dt_end = date(2020, 9, 1)

    res2 = retrieve_station_measurements(api, station_name, parameter, dt_begin, dt_end)

    return res2


if __name__ == "__main__":
    main()
    