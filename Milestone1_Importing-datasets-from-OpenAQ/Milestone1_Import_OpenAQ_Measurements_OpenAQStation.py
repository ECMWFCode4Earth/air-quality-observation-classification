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



def Milestone1_Get_OpnenAQ_Dataset_Measurement_perStation(OpenAQStation, parameter):
    
#Step 1 Choose the measurement country to import and parameter 
   res1 = api.measurements(location=OpenAQStation, parameter=parameter, limit=10000, df=True)

   return res1

print("Get the OpenAQ measurements for one chosen OpenAQ")

#Step 1 Choose the measurement country to import and parameter
#
# Choose the country on the country code
#
# OpenAQCountry = 'IN'

     
OpenAQCountry = 'US Diplomatic Post: Abu Dhabi'

print("Country Chosen ")

print(OpenAQCountry)

print("Parameter chosen")

parameter = 'pm25'

print(parameter)

api = openaq.OpenAQ()

Measurements1 = Milestone1_Get_OpnenAQ_Dataset_Measurement_perStation(OpenAQCountry, parameter)

print(Measurements1)
