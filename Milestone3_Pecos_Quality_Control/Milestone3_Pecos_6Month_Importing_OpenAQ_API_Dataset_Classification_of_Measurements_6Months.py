# -*- coding: utf-8 -*-
"""
Created on Tue Oct 27 09:49:49 2020

@author: wegia
"""

import openaq
import pandas as pd
from pandas.io.json import json_normalize
import pecos
import matplotlib.pyplot as plt
from datetime import datetime, date, time, timezone


api = openaq.OpenAQ()

status, resp = api.cities()


dt_begin = date(2020,3,1)
dt_end = date(2020,9,1)

dt_start = date.today()

#date_to

print(dt_begin)
print(dt_start)
#Step 1 Choose the measurement country to import and parameter
res1 = api.measurements(country='IN', parameter='pm25', date_to=dt_end, date_from=dt_begin, limit=10000, df=True)

res_1 = api.measurements(location='US Diplomatic Post: Hyderabad', parameter='pm25', date_to=dt_end, date_from=dt_begin, limit=10000, df=True)

# 
print(res_1.dtypes)


#res_1['date.utc'] = pd.to_datetime(res1['date.utc']).dt.tz_localize(None)

res_1 = res_1[res_1.value != -999.00]

res_1.set_index('date.utc')

print(res_1)
print(res_1['value'])

print(res_1['date.utc'])


print(res_1['value'])

# Step 2 Initialize logger and Create a Pecos PerformanceMonitoring data object
pecos.logger.initialize()
 
pm = pecos.monitoring.PerformanceMonitoring()


# Step 3 Append Dataframe to Pecos PerformanceMonitoring data object
pm.add_dataframe(res_1)
#pm.add_translation_dictionary({'Wave': ['value_copy1','value_copy2']}) # group C and D


# Step 4 Check the expected frequency of the timestamp
pm.check_timestamp(900)
  

# Step 5 Check for missing data
pm.check_missing()
        
#pm.check_corrupt([-999, 999],key='value')

# Step 6 Choose acceptable value range and Check data for expected ranges
#
# Parameters
#  
#  1 Lower bound of values
#  2 Higher Bound of values
#  3 Data column (default = None, which indicates that all columns are used)
#  4 Minimum number of consecutive failures for reporting (default = 1)le increment from measurements of 15 minutes and check for abrupt changes between consecutive time steps
#
#   e.g pm.check_range([0, 200], key='value')  
#         pm.check_range([1, 2], key='3',4)
#
# Results: Any value outside of the range is an outlier

pm.check_range([0, 200], key='value')
  
# Step 7 Choose the min amount that is acceptable to change from measurements 
#
# Parameters:
#
#    1 Lower bound to decrease by
#    2 Upper bound to increase by
#    3 Size of the moving window used to compute the difference between the minimum and maximum
#    4 Data column (default = None, which indicates that all columns are used)
#    5 Flag indicating if the test should only check for positive delta (the min occurs before the max) or negative delta (the max occurs before the min) (default = False)
#    6 Minimum number of consecutive failures for reporting (default = 1)

#  e.g. pm.check_delta([Miniumn Decrease, Min Increase], window=3600, 'value')
#      included parametes 1-6: pm.check_delta([1, 2], window=3, key='4', 5, 6)
#
#  Results: When over min decrease or increase it is an outlier


pm.check_delta([None, 10], window=3600, key='value')

# Step 8 Choose acceptable increment on measurements 
#
# Parameters
#  
#  1 Lower bound to de increment by
#  2 Higher Bound to increment by
#  3 Data column (default = None, which indicates that all columns are used)
#  4 Increment used for difference calculation (default = 1 timestamp)
#  5 Flag indicating if the absolute value of the increment is used in the test (default = True)
#  6 Minimum number of consecutive failures for reporting (default = 1)
#
# e.g pm.check_increment([None, 20], 'value') 
#    included parametes 1- 4:  pm.check_increment([1, 2], key='3', 4, 5, 6) 
#
# Results: Any measurement that has a larger increment or de increment by choosen value is an outlier

pm.check_increment([None, 20], key='value') 


# Step 9 Compute the quality control index for value
mask = pm.mask[['value']]
QCI = pecos.metrics.qci(mask, pm.tfilter)


# Step 10 Generate graphics
test_results_graphics = pecos.graphics.plot_test_results(pm.df, pm.test_results)
res_1.plot(y='value', ylim=[1,100], figsize=(7.0,3.5))
plt.savefig('custom.png', format='png', dpi=500)

print(pm.test_results)
# Step 11 Write test results and report files to test_results.csv and monitoringreport.html
pecos.io.write_test_results(pm.test_results,filename='test_results.csv')
pecos.io.write_monitoring_report(pm.df, pm.test_results, test_results_graphics, 
                                 ['custom.png'], QCI,filename='monitoring_report.html')


