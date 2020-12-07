# -*- coding: utf-8 -*-
"""
Created on Tue Dec  1 15:12:57 2020

@author: wegia
"""



import openaq

import pandas as pd

import pecos

import seaborn as sns

from pandas import json_normalize

import matplotlib.pyplot as plt

from datetime import datetime, date, time, timezone

import numpy as np

import csv

# Step 1 Initiatlise pyOpenAQ API
#
#  1 There are no edits 

print("  STEP 1 ")

print("********")

print("Initialise pyOpenAQ API")

api = openaq.OpenAQ()


print("OpenAQ pyOpenAPI begun")


def Milestone1_Get_OpenAQStation_Latlng(OpenAQStationCountry):
    
    
   OpenAQLatLng = api.locations(location=OpenAQStationCountry, df=True)

   OpenAQLatlngDataset = []


   print(OpenAQLatLng)
   
   OpenAQLatlngDataset.append(OpenAQLatLng['coordinates.latitude'])
 
   OpenAQLatlngDataset.append(OpenAQLatLng['coordinates.longitude'])

   return OpenAQLatlngDataset


def Milestone1_Get_OpnenAQ_Dataset_Measurement_perStation(StationOpenAQCoordinates, Radius, parameter, dt_begin, dt_end):
    
#Step 1 Choose the measurement country to import and parameter 
    
#   res1 = api.measurements(location=StationOpenAQ, parameter=parameter, date_to=dt_end, date_from=dt_begin, limit=10000, df=True)

   measure = ""

#   res1 = api.measurements(coordinates="24.4244,54.43375", parameter=parameter, radius=250000, date_to=dt_end, date_from=dt_begin, df=True, limit=10000)

   res1 = api.measurements(coordinates=StationOpenAQCoordinates, parameter=parameter, radius=Radius, date_to=dt_end, date_from=dt_begin, df=True, limit=10000)


   print("Completed measurements ")

   return res1



def Milestone2_Get_OpenAQ_Dataset_Wrangling_utc_index(OpenAQ_Dataset_ImportAPI):

   format = '%Y-%m-%d %H:%M:%S'
    
   OpenAQ_Dataset_ImportAPI['date.utc'] = pd.to_datetime(OpenAQ_Dataset_ImportAPI['date.utc'], format=format).dt.tz_localize(None)

   OpenAQ_Dataset_ImportAPI = OpenAQ_Dataset_ImportAPI[OpenAQ_Dataset_ImportAPI.value != -999.00]

   Formating = pd.DatetimeIndex(OpenAQ_Dataset_ImportAPI['date.utc'])
                 
 
   
   OpenAQ_Dataset_ImportAPI = OpenAQ_Dataset_ImportAPI.set_index(Formating)

  # OpenAQ_Dataset_ImportAPI = OpenAQ_Dataset_ImportAPI.set_index('date.utc')

  # print(OpenAQ_Dataset_ImportAPI)

 #  print(OpenAQ_Dataset_ImportAPI['value'])

  # print(OpenAQ_Dataset_ImportAPI['date.utc'])


 #  print(OpenAQ_Dataset_ImportAPI['value'])

   return OpenAQ_Dataset_ImportAPI
   


def Milestone2_Remove_neg_attribute(OpenAQ_Dataset_ImportAPI):
    
    OpenAQ_Dataset_ImportAPI = OpenAQ_Dataset_ImportAPI[OpenAQ_Dataset_ImportAPI.value != -999.00]

    return OpenAQ_Dataset_ImportAPI

def Milestone2_Remove_negative_attribute(OpenAQ_Dataset_ImportAPI):
    
    OpenAQ_Dataset_ImportAPI = OpenAQ_Dataset_ImportAPI[OpenAQ_Dataset_ImportAPI.value >= 0]

    return OpenAQ_Dataset_ImportAPI

def Milestone2_OpenAQ_Dataset_VisualAnalytics_Histogram_Unique(df4, OpenAQStationunique, xaxis, yaxis, parameter, OpenAQDataset_VisualAnalytics, xlabel='Value', ylabel='Amount of Measurements', dpi=100):
   
   for OpenAQunique in OpenAQStationunique:
        
      print(OpenAQunique) 
       
      OpenAQAPIdatasetunique = df4[df4['location'] == OpenAQunique]
      
      Milestone2_OpenAQ_Dataset_VisualAnalytics_Histogram(OpenAQAPIdataset, parameter, title=OpenAQDataset_VisualAnalytics, xlabel='Value', ylabel='Amount of Measurements', dpi=100)
      
      Milestone2_Import_OpenAQ_CSV_plot(OpenAQAPIdataset, xaxis, yaxis, parameter, title=OpenAQDataset_VisualAnalytics, xlabel='Value', ylabel='Amount of Measurements', dpi=100)


def Milestone2_Import_OpenAQ_CSV_plot_Unique(df4, OpenAQStationunique, xaxis, yaxis, parameter, OpenAQDataset_VisualAnalytics, xlabel='Value', ylabel='Amount of Measurements', dpi=100):
   
   for OpenAQunique in OpenAQStationunique:
        
      print(OpenAQunique) 
       
      OpenAQAPIdatasetunique = df4[df4['location'] == OpenAQunique]
      
      Milestone2_Import_OpenAQ_CSV_plot(OpenAQAPIdataset, xaxis, yaxis, parameter, title=OpenAQDataset_VisualAnalytics, xlabel='Value', ylabel='Amount of Measurements', dpi=100)


def Milestone2_OpenAQ_Dataset_VisualAnalytics_Histogram(df4, parameter, title="", xlabel='Value', ylabel='Amount of Measurements', dpi=100):
    
# Step Create a Histogram of the OpenAQ Dataset for parameter
   
   print("Histrgram of OpenAQ Dataset from OpenAQ API download") 
    
   plt.gca().set(title=title, xlabel=xlabel, ylabel=ylabel)
   
   plt.hist(df4['value'], bins=np.arange(1,df4['value'].max()))
   plt.show()


def Milestone2_Import_OpenAQ_CSV_plot(df4, xaxis, yaxis, parameter, title="", xlabel='Date', ylabel='Value', dpi=100):
    
    
    
    print("OpenAQ Dataset LinePlot")
     
    plt.figure(figsize=(16,5), dpi=dpi)
    plt.plot(xaxis, yaxis, color='tab:blue')
    plt.gca().set(title=title, xlabel=xlabel, ylabel=ylabel)
   
    plt.show()



def Milestone2_Import_OpenAQ_Line_Stations(res):

   fig, ax = plt.subplots(1, figsize=(10, 6))

   for group, df in res.groupby('location'):
    # Query the data to only get positive values and resample to hourly
      _df = df.query("value >= 0.0").resample('1h').mean()

      _df.value.plot(ax=ax, label=group)

      ax.legend(loc='best')
      ax.set_ylabel("$PM_{2.5}$  [$\mu g m^{-3}$]", fontsize=20)
      ax.set_xlabel("")
      sns.despine(offset=5)

      plt.legend(bbox_to_anchor=(1.05, 1), loc=2, borderaxespad=0.)

      plt.show()


def Milestone2_Import_OpenAQ_Scatter(Xaxis_Measurement, Yaxis, parameter, title, xlabel, ylabel):
    
   fig, ax = plt.subplots()
   scale = 200.0 
   ax.scatter(Xaxis_Measurement, Yaxis, c='tab:blue', s=scale, label=parameter, alpha=0.3, edgecolors='none')
   
   ax.legend()
   ax.grid(True)
   plt.gca().set(title=title, xlabel=xlabel, ylabel=ylabel)
   
   plt.show()


def Milestone3_Pecos_Complete_QualityControl_One_OpenAQStation(OpenAQStation, OpenAQStation_Dataset, iteration_OpenAQStations):

   # Step 2 Initialize logger and Create a Pecos PerformanceMonitoring data object
   pecos.logger.initialize()
 
   pm = pecos.monitoring.PerformanceMonitoring()


   # Step 3 Append Dataframe to Pecos PerformanceMonitoring data object
   pm.add_dataframe(OpenAQStation)

   # Step 4 Check the expected frequency of the timestamp
   #
   # 1 Edit timestep when 900 is 15 mins     

   Timestep = 900 # Edit
   
   pm.check_timestamp(Timestep)

   print("*****")

   print("Criteria 1 : Timestep ")
   
   
   
   print(Timestep)
   
  
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

   LowerBound = None # Edit 
   
   HigherBound = 200 # Edit

   pm.check_range([LowerBound, HigherBound], key='value')
 

   print("*****")
   
   print("Criteria 2 : Lower Bound and Higher Bound ")
  
   print("Lower Bound ")
   
   print(LowerBound)   
   
   print("Higher Bound")
   
   print(HigherBound)
   
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
 
   print("*****")
 
   
   print("Criteria 3 : Stagnant Measurements ")
  
   DeltaLowerBound = None # Edit
   
   DeltaHigherBound = 10 # Edit
   
   DeltaTimeSchedule = 3600 # Edit
   
   pm.check_delta([DeltaLowerBound, DeltaHigherBound], window=DeltaTimeSchedule, key='value')

   print(" Measurement that increase by " )
   
   print(DeltaHigherBound )
   
   print("in Time Schedule")
   
   print(DeltaTimeSchedule)

   print("Delta Lower Bound")

   print(DeltaLowerBound)

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

   print("*****")
 
   print("Criteria 3 : Stagnant Measurements ")

   Increment_Increase = 20 # Edit
   
   Increment_Decrease = None # Edit
  
   pm.check_increment([None, 20], key='value') 

   print("Increment Increase")
   
   print(Increment_Increase)

   print("Increment Decrease")
   
   print(Increment_Decrease)


   pm.check_outlier([None, 3], window=12*3600)

   # Step 9 Compute the quality control index for value
   mask = pm.mask[['value']]
   QCI = pecos.metrics.qci(mask)

   print("*****")

   print("OpenAQ Dataset Results ")

   print("Mask")
  
   print(mask) 
   
   print("Performance Metrics")

   print(QCI)

   custom = 'custom' + iteration_OpenAQStations + '.png'

   MeasurementOpenAQ = int(OpenAQStation['value'].max())

   print(OpenAQStation['value'].describe())
  
  # Step 10 Generate graphics
   test_results_graphics = pecos.graphics.plot_test_results(pm.df, pm.test_results)
   OpenAQStation.plot(y='value', ylim=[0,MeasurementOpenAQ], figsize=(7.0,3.5))
   plt.savefig(custom, format='png', dpi=500)

   print(pm.test_results)

   # Step 11 Write test results and report files to test_results.csv and monitoringreport.html

   Report = 'test_results' + OpenAQStation_Dataset + iteration_OpenAQStations + '.csv' 

   MonitoringReport = 'MonitoringReport' + OpenAQStation_Dataset + iteration_OpenAQStations + '.html'

   pecos.io.write_test_results(pm.test_results,filename=Report)
   pecos.io.write_monitoring_report(pm.df, pm.test_results, test_results_graphics, 
                                 [custom], QCI,filename=MonitoringReport)

   return pm.test_results



def Milestone4_Get_NearestHighway_OpenAQStations():
  
   OpenAQ_Dataset_LatlngCSV_Download = "OpenAQLatlngNearestHighway.csv"

    
   OpenAQdatasetsLatLng = []
   
   delimiterOpenAQ = ','
   with open(OpenAQ_Dataset_LatlngCSV_Download,'r') as dest_f:
    data_iter = csv.reader(dest_f, delimiter=delimiterOpenAQ)
    
    for dataset in data_iter:
       OpenAQdatasetsLatLng.append(dataset)
   #    print(dataset)
       
  #  OpenAQDataset = np.asarray(OpenAQdatasetsLatLng)
   
   
   return OpenAQdatasetsLatLng

def Milestone4_Get_NearestHighway_OpenAQStations_OneStation(OpenAQLatlng, OpenAQdatasetsLatLng):
  
 
   OpenAQStation_NearestDistance = 0;

   for OpenAQStationLatlng in OpenAQdatasetsLatLng[0]:
   
    #  print(" OpenAQ ")
      
    #  print(OpenAQStationLatlng)
 #     print(OpenAQLatlng[0])
      
      OpenAQStationDatasetLatlng = OpenAQStationLatlng.split('?')
   #   print(OpenAQLatlng[0])
   #   print(OpenAQLatlng[1][0])
      
   #   print(OpenAQLatlng[1][0])
      
   #   print(OpenAQStationDatasetLatlng)   
      if(float(OpenAQStationDatasetLatlng[0]) == float(OpenAQLatlng[0][0])):
          if(float(OpenAQStationDatasetLatlng[1]) == float(OpenAQLatlng[1][0])):
            OpenAQStation_NearestDistance = OpenAQStationDatasetLatlng
  #          print(OpenAQStationLatlng[0])
   #         print(OpenAQLatlng[0])
      
   print(OpenAQStation_NearestDistance)
 #  print(OpenAQLatlng[0][0])
 #  print(OpenAQLatlng[1][0])
   
   
   
   return OpenAQStation_NearestDistance

def Milestone4_Get_NearestHighway_OpenAQStations_Station(df4, parameter, OpenAQStationunique):
   
   OpenAQAPIdatasetuniqueDataset = [] 
    
     
   OpenAQAPIuniqueDataset = [] 
 
   OpenAQNearestHighway = Milestone4_Get_NearestHighway_OpenAQStations() 
   
   for OpenAQunique in OpenAQStationunique:
        
      print(OpenAQunique) 
      
      OpenAQStationLatlng = Milestone1_Get_OpenAQStation_Latlng(OpenAQunique)
  
      OpenAQAPIdatasetunique = df4[df4['location'] == OpenAQunique]
      
   #   print(OpenAQAPIdatasetunique)
      
      OpenAQStationLatlng_NearestHighway = Milestone4_Get_NearestHighway_OpenAQStations_OneStation(OpenAQStationLatlng, OpenAQNearestHighway)

      print(OpenAQAPIdatasetunique['value'].describe())

      print("Distance to the nearest Highway in Km ")
      if(OpenAQStationLatlng_NearestHighway != 0):
        if(len(OpenAQStationLatlng_NearestHighway) == 6):
          print(OpenAQStationLatlng_NearestHighway[5])

          OpenAQAPIuniqueDataset.append(OpenAQStationLatlng_NearestHighway[5])
        else:
          OpenAQAPIuniqueDataset.append(0)
     
          
      OpenAQAPIdatasetuniqueDataset.append(OpenAQAPIdatasetunique['value'].describe()['mean'])

  # print("For these OpenAQ Stations")
  
   print(OpenAQAPIuniqueDataset)
   
   print(OpenAQAPIdatasetuniqueDataset)
   
   # Milestone2_Import_OpenAQ_CSV_plot(OpenAQStationunique, OpenAQAPIuniqueDataset, OpenAQAPIdatasetuniqueDataset, parameter, title="Distance Nearest Highway", xlabel='Distance to Nearest Highway in Km', ylabel='Mean of Measurements', dpi=100)

   title="Distance Nearest Highway"
   
   xlabel='Distance to Nearest Highway in Km'
   
   ylabel='Mean of Measurements'
   
   Milestone2_Import_OpenAQ_Scatter(OpenAQAPIuniqueDataset, OpenAQAPIdatasetuniqueDataset, parameter, title, xlabel, ylabel)
   
   


print("Get the OpenAQ measurements for stations within raduis of chosen Coordinates from OpenAQ and doing Quality Control on it")

#Step 1 Choose the measurement country to import and parameter
#
# Choose the station
#
# OpenAQStationCountry = ''


print("  STEP 1 ")

print("********")

print("Chosen OpenAQ Coordinates and Radius: ")
     
OpenAQStationCountry = "24.4244,54.43375" #Edit

Radius = 25000 # Edit in metres 

OpenAQStationdfDatasetCountry = 'US Diplomatic Post Abu Dhabi'

print(OpenAQStationCountry)


print("Completed Step 1 ")

print(">")

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



# Step 5 Get Measurements from openAQ API 
#
#
# Test 
#
#resp = api.cities(df=True, limit=10000)

#res1 = api.measurements(city='Delhi', df=True, limit=10000)

print("  STEP 5 ")

print("********")

print("Getting Measurements from OpenAQ API source")

res2 = Milestone1_Get_OpnenAQ_Dataset_Measurement_perStation(OpenAQStationCountry, Radius, parameter, dt_begin, dt_end)

print("Found these Stations in Coordinates")

OpenAQStationunique = res2['location'].unique()

print(OpenAQStationunique)


#print(Measurements1)

# Step 6 Choose to remove measurement that have -999.00
#
# 1 It only removes -999.0 that are missing measurements 
#
#  Edit the Remove_Neg to either
#
#   1 - Remove -999.0 from dataset 
# 
#   0 - Don't remove -999.0 from dataset
#
#  i.e Change to chosen
# 
#   Remove_Neg = 1
#
#  2 Choose to remove negative measurements 
#
#  Change  Remove_Negative_Measurements
#  
#   1 - Remove negative measurements 


print("  STEP 6 ")

print("********")

print("Choose to remove missing measurements that are -999.0 and below 0")

Remove_Neg = 1 # Edit      Removes Only measurements of -999.0 

Remove_Negative_Measurements = 1 # Edit Remove measure below 0 

Remove_Neg_NO = 0

Remove_Neg_YES = 1

if(Remove_Neg == Remove_Neg_YES):
  res2 = Milestone2_Remove_neg_attribute(res2)
  print("Removing missing measurements that are -999.0")
else:
  print("Not removing missing measurements that are -999.0")  
  
if(Remove_Negative_Measurements == Remove_Neg_YES):
  res2 = Milestone2_Remove_negative_attribute(res2)
  print("Removing measurement below 0")
  
  
# Step 7 Do Data Wrangling on OpenAQ dataset  
#
# 1 It convert utc to DateTime for Pecos Quality Control and utc to index
#
#   
  

print("  STEP 7 ")

print("********")
  
print("Data Wrangling OpenAQ dataset evaluating UTC date to Date format and setting utc to index")
  
res2 = Milestone2_Get_OpenAQ_Dataset_Wrangling_utc_index(res2)

print("Dataset Wrangling Completed")

print("OpenAQ Dataset imported ")

print(res2.dtypes)


# Step 8 Import just Measurements to Dataframe with Date utc index for applying 

print("  STEP 8 ")

print("********")

print("Get measurement to Dataframe")
  
OpenAQAPIdataset = pd.DataFrame(res2, columns=['value','location'])


# Step 10 Completing the Pecos Quality Control 
#
#  1 The Search Criteria are edited in the Method 
#
#  Milestone3_Pecos_Complete_QualityControl_One_OpenAQStation
#
#  2 The iteration can be change to document every time it is processed 
#
#   iteration_OpenAQStations = '0'

#Step 9 Plot OpenAQ Dataset to Line plot and Histogram

print("  STEP 9 ")

print("********")

print("Graph of OpenAQ Dataset Measumrents")


Milestone2_Import_OpenAQ_Line_Stations(res2)

OpenAQDataset_VisualAnalytics = "OpenAQ Dataset Station " + OpenAQStationdfDatasetCountry + " " + parameter + " Time Schedule " + str(dt_begin) + " to " + str(dt_end)

Milestone2_OpenAQ_Dataset_VisualAnalytics_Histogram_Unique(OpenAQAPIdataset, OpenAQStationunique, OpenAQAPIdataset.index, OpenAQAPIdataset['value'], parameter, OpenAQDataset_VisualAnalytics, xlabel='Value', ylabel='Amount of Measurements', dpi=100)

print("  STEP 10 ")

print("********")

print("Get Pecos Quality Control on OpenAQ dataset")

print("Iteration ")


iteration_OpenAQStations = '0'  #Edit 

print(iteration_OpenAQStations)

print("OpenAQ Pecos Quality Control Search Criteria: ")

print(" **** ")

Milestone3_Pecos_Complete_QualityControl_One_OpenAQStation(OpenAQAPIdataset,  OpenAQStationdfDatasetCountry, iteration_OpenAQStations)

print("  STEP 11 ")

print("********")

print("Get Distance to Nearest Highway")


# OpenAQStationLatlng = Milestone1_Get_OpenAQStation_Latlng(OpenAQStationCountry)

# OpenAQStationLatlng_NearestHighway = Milestone4_Get_NearestHighway_OpenAQStations(OpenAQStationLatlng)

# print(OpenAQAPIdataset['value'].describe())

print("Distance to the nearest Highway in Km ")

# print(OpenAQStationLatlng_NearestHighway[4])

Milestone4_Get_NearestHighway_OpenAQStations_Station(OpenAQAPIdataset, parameter, OpenAQStationunique)


