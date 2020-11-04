# -*- coding: utf-8 -*-
"""
Created on Wed Nov  4 14:52:17 2020

@author: wegia
"""




import openaq

import pandas as pd


from pandas.io.json import json_normalize

import matplotlib.pyplot as plt

from datetime import datetime, date, time, timezone



def Milestone1_Get_OpnenAQ_Dataset_Measurement_perCountry(OpenAQCountry, parameter):

    print("Milestone1_Get_OpnenAQ_Dataset_Measurement_perCountry(OpenAQCountry)")

    res1 = api.measurements(country=OpenAQCountry, parameter=parameter, limit=10000, df=True)

    print("Completed Milestone1_Get_OpnenAQ_Dataset_Measurement_perCountry(OpenAQCountry)")

    return res1   

print("Get the OpenAQ measurements for one chosen country")

#Step 1 Choose the measurement country to import and parameter
#
# Choose the country on the country code
#
# OpenAQCountry = 'IN'

     
OpenAQCountry = 'IN'

print("Country Choosen ")

print(OpenAQCountry)

print("Chosen parameter")

parameter = 'pm25'

print(parameter)

api = openaq.OpenAQ()

Milestone1_Get_OpnenAQ_Dataset_Measurement_perCountry(OpenAQCountry, parameter)
