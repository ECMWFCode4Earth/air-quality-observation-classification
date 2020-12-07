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




def Milestone2_Remove_neg_attribute(OpenAQ_Dataset_ImportAPI):
    
    OpenAQ_Dataset_ImportAPI = OpenAQ_Dataset_ImportAPI[OpenAQ_Dataset_ImportAPI.value != -999.00]

    return OpenAQ_Dataset_ImportAPI


def Milestone1_Get_OpnenAQ_Dataset_Measurement_perStation(StationOpenAQ, parameter):
    
#Step 1 Choose the measurement country to import and parameter 
    
   res1 = api.measurements(location=StationOpenAQ, parameter=parameter, date_to=dt_end, date_from=dt_begin, limit=10000, df=True)

   print("Completed measurements ")

   return res1



def Milestone2_Get_OpenAQ_Dataset_Wrangling_utc_index(OpenAQ_Dataset_ImportAPI):

   format = '%Y-%m-%d %H:%M:%S'
    
   OpenAQ_Dataset_ImportAPI['date.utc'] = pd.to_datetime(OpenAQ_Dataset_ImportAPI['date.utc'], format=format).dt.tz_localize(None)

   OpenAQ_Dataset_ImportAPI = OpenAQ_Dataset_ImportAPI[OpenAQ_Dataset_ImportAPI.value != -999.00]

   Formating = pd.DatetimeIndex(OpenAQ_Dataset_ImportAPI['date.utc'])
                 
 
   
   OpenAQ_Dataset_ImportAPI = OpenAQ_Dataset_ImportAPI.set_index(Formating)

  # OpenAQ_Dataset_ImportAPI = OpenAQ_Dataset_ImportAPI.set_index('date.utc')

   print(OpenAQ_Dataset_ImportAPI)

   print(OpenAQ_Dataset_ImportAPI['value'])

   print(OpenAQ_Dataset_ImportAPI['date.utc'])


 #  print(OpenAQ_Dataset_ImportAPI['value'])

   return OpenAQ_Dataset_ImportAPI
   



def Milestone3_Pecos_Complete_QualityControl_One_OpenAQStation(OpenAQStation, OpenAQStation_Dataset, iteration_OpenAQStations):

   # Step 2 Initialize logger and Create a Pecos PerformanceMonitoring data object
   pecos.logger.initialize()
 
   pm = pecos.monitoring.PerformanceMonitoring()


   # Step 3 Append Dataframe to Pecos PerformanceMonitoring data object
   pm.add_dataframe(OpenAQStation)

   # Step 4 Check the expected frequency of the timestamp
   pm.check_timestamp(900)
  
   # Step 5 Check for missing data
   pm.check_missing()
        

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

   custom = 'custom' + iteration_OpenAQStations + '.png'

   

   MeasurementOpenAQ = int(OpenAQStation['value'].max())

   # Step 10 Generate graphics
   test_results_graphics = pecos.graphics.plot_test_results(pm.df, pm.test_results)
   OpenAQStation.plot(y='value', ylim=[1,MeasurementOpenAQ], figsize=(7.0,3.5))
   plt.savefig(custom, format='png', dpi=500)

   print(pm.test_results)

   # Step 11 Write test results and report files to test_results.csv and monitoringreport.html

   Report = 'test_results' + OpenAQStation_Dataset + iteration_OpenAQStations + '.csv' 

   MonitoringReport = 'MonitoringReport' + OpenAQStation_Dataset + iteration_OpenAQStations + '.html'

   pecos.io.write_test_results(pm.test_results,filename=Report)
   pecos.io.write_monitoring_report(pm.df, pm.test_results, test_results_graphics, 
                                 [custom], QCI,filename=MonitoringReport)

   return pm.test_results



print("Get the OpenAQ measurements for one chosen OpenAQ and doing Quality Control on it")

#Step 1 Choose the measurement country to import and parameter
#
# Choose the station
#
# OpenAQStationCountry = ''


print("  STEP 1 ")

print("********")

print("Chosen OpenAQ Station: ")
     
OpenAQStationCountry = 'US Diplomatic Post: Abu Dhabi'


OpenAQStationdfDatasetCountry = 'US Diplomatic Post Abu Dhabi'

print(OpenAQStationCountry)

# Step 2 Choose parameter

print("  STEP 2 ")

print("********")


print("Parameter chosen")

parameter = 'pm25'

print(parameter)


#Step 3 Choose time schedule 
#
# 
# 1 Change Time Schedule from 6 months to other in dt_begin
#  and dt_end
#
#  dt_begin =  date(2020,3,1) 1 March 2020 
#
#  dt_end =  date(2020,9,1) 1 September 2020

dt_begin = date(2020,3,1) # Edit

dt_end = date(2020,9,1) # Edit

# dt_start = date.today()

print("  STEP 3 ")

print("********")


print("Getting OpenAQ dataset applying pyOpenAQ API from ") 
print(dt_begin)
print(" to ")
print(dt_end)
print(" for one OpenAQ Station and one parameter ")

# Step 4 Inituial pyOpen API 
#
#  1 There are no edits 

print("  STEP 4 ")

print("********")


api = openaq.OpenAQ()

print("OpenAQ pyOpenAPI begun")

# Step 5 Get Measurements from openAQ API 
#
#


#res1 = api.measurements(coordinates=40.23,34.17, df=True, limit=10000)
#resp = api.cities(df=True, limit=10000)

#res1 = api.measurements(city='Delhi', df=True, limit=10000)

print("  STEP 5 ")

print("********")

print("Getting Measurements from OpenAQ API source")

res2 = Milestone1_Get_OpnenAQ_Dataset_Measurement_perStation(OpenAQStationCountry, parameter)

#print(Measurements1)

# Step 6 Choose to remove measurement that have -999.00
#
# 1 It only removes -999.0 that are missing measurements 
#
# 

Remove_Neg = 0; # Only measurements of -999.0 

Remove_Neg_NO = 0

Remove_Neg_YES = 1

if(Remove_Neg == Remove_Neg_YES):
  res2 = Milestone2_Remove_neg_attribute(res2)


res2 = Milestone2_Get_OpenAQ_Dataset_Wrangling_utc_index(res2)


res1 = res2

print(res1.dtypes)


res1 = res2

print(res1.dtypes)


OpenAQAPIdataset = pd.DataFrame(res1, columns=['value'])

iteration_OpenAQStations = '0'

Milestone3_Pecos_Complete_QualityControl_One_OpenAQStation(OpenAQAPIdataset,  OpenAQStationdfDatasetCountry, iteration_OpenAQStations)




