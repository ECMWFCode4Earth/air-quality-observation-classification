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

api = openaq.OpenAQ()

status, resp = api.cities()

#Step 1 Choose the measurement country to import and parameter
res1 = api.measurements(country='IN', parameter='pm25', limit=10000, df=True)


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
pm.check_timestamp(900)
    


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
pecos.io.write_test_results(pm.test_results,filename='test_result.csv')
pecos.io.write_monitoring_report(pm.df, pm.test_results, test_results_graphics, 
                                 ['custom.png'], QCI,filename='monitoring_report.html')


