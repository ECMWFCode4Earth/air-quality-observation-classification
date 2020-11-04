# -*- coding: utf-8 -*-
"""
Created on Wed Nov  4 14:52:17 2020

@author: wegia
"""




import openaq

import pandas as pd

import pecos

from pandas.io.json import json_normalize

import matplotlib.pyplot as plt

from datetime import datetime, date, time, timezone



def Milestone1_Get_OpnenAQ_Dataset_Measurement_perStation(OpenAQStation, parameter):
    
#Step 1 Choose the measurement country to import and parameter 
   res1 = api.measurements(location=OpenAQStation, parameter=parameter, limit=10000, df=True)

   return res1

print("Get the OpenAQ measurements for one chosen OpenAQ and doing Quality Control on it")

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

res2 = Milestone1_Get_OpnenAQ_Dataset_Measurement_perStation(OpenAQCountry, parameter)

#print(Measurements1)

res1 = res2

print(res1.dtypes)

res1.set_index('date.utc')

print(res1['value'])

res1['date.utc'] = pd.to_datetime(res1['date.utc']).dt.tz_localize(None)
# Step 2 Initialize logger
pecos.logger.initialize()

# Step 3 Create a Pecos PerformanceMonitoring data object
pm = pecos.monitoring.PerformanceMonitoring()


# Step 4 Append Dataframe to Pecos PerformanceMonitoring data object
pm.add_dataframe(res1)
#pm.add_translation_dictionary({'Wave': ['value_copy1','value_copy2']}) # group C and D


# Step 5 Check for missing data
pm.check_missing()
        

# Step 6 Choose acceptable value range and Check data for expected ranges
pm.check_range([0, 200], 'value')

# Step 7 Check the expected frequency of the timestamp
#pm.check_timestamp(900)
    


# Step 8 Choose acceptable increment from measurements of 15 minutes and check for abrupt changes between consecutive time steps
pm.check_increment([None, 20], 'value') 


# Step 9 Compute the quality control index for value
mask = pm.mask[['value']]
QCI = pecos.metrics.qci(mask, pm.tfilter)


# Step 10 Generate graphics
test_results_graphics = pecos.graphics.plot_test_results(pm.df, pm.test_results)
#res1.plot(ylim=[1,100], figsize=(7.0,3.5))
plt.savefig('custom.png', format='png', dpi=500)

print(pm.test_results)
# Step 11 Write test results and report files to test_results.csv and monitoringreport.html
pecos.io.write_test_results(pm.test_results,filename='test_resultcsv1.csv')
pecos.io.write_monitoring_report(pm.df, pm.test_results, test_results_graphics, 
                                 ['custom.png'], QCI,filename='monitoring_report1.html')




