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



def Milestone1_Get_OpenAQStation_Latlng(OpenAQStationCountry):
    
    
   OpenAQLatLng = api.locations(location=OpenAQStationCountry, df=True)

   OpenAQLatlngDataset = []


   print(OpenAQLatLng)
   
   OpenAQLatlngDataset.append(OpenAQLatLng['coordinates.latitude'])
 
   OpenAQLatlngDataset.append(OpenAQLatLng['coordinates.longitude'])

   return OpenAQLatlngDataset


def Milestone1_Get_OpnenAQ_Dataset_Measurement_perStation(StationOpenAQCoordinates, Radius, parameter, dt_begin, dt_end):
    
#Step 1 Choose the measurement country to import and parameter 
   
   res1 = api.measurements(coordinates=StationOpenAQCoordinates, parameter=parameter, radius=Radius, date_to=dt_end, date_from=dt_begin, df=True, limit=10000)

   print("Completed measurements ")

   return res1



def Milestone2_Get_OpenAQ_Dataset_Wrangling_utc_index(OpenAQ_Dataset_ImportAPI):

   format = '%Y-%m-%d %H:%M:%S'
    
   OpenAQ_Dataset_ImportAPI['date.utc'] = pd.to_datetime(OpenAQ_Dataset_ImportAPI['date.utc'], format=format).dt.tz_localize(None)

   OpenAQ_Dataset_ImportAPI = OpenAQ_Dataset_ImportAPI[OpenAQ_Dataset_ImportAPI.value != -999.00]

   Formating = pd.DatetimeIndex(OpenAQ_Dataset_ImportAPI['date.utc'])
      
   OpenAQ_Dataset_ImportAPI = OpenAQ_Dataset_ImportAPI.set_index(Formating)


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


def Milestone2_Import_OpenAQ_Scatter(Xaxis_Measurement, Yaxis, parameter, title, xlabel, ylabel):
    
   fig, ax = plt.subplots()
   scale = 200.0 
   ax.scatter(Xaxis_Measurement, Yaxis, c='tab:blue', s=scale, label=parameter, alpha=0.3, edgecolors='none')
   
   ax.legend()
   ax.grid(True)
   plt.gca().set(title=title, xlabel=xlabel, ylabel=ylabel)
   
   plt.show()


def Milestone3_Get_Imported_OpenAQ_Dataset(): 
    
   OpenAQ_Dataset_LatlngCSV_Download = '../Milestone1_Importing-datasets-from-OpenAQ/OpenAQ_Dataset Unique selection pm25 CoordinateCentreandRadius 2020-03-01 to 2020-09-01.csv'

   OpenAQdatasetsLatLng = []
   ImportOpenAQimported = pd.read_csv(OpenAQ_Dataset_LatlngCSV_Download)
    
   delimiterOpenAQ = ' '
   with open(OpenAQ_Dataset_LatlngCSV_Download,'r') as dest_f:
       
    
    data_iter = csv.reader(dest_f, delimiter=delimiterOpenAQ)
    
    for dataset in data_iter:
       OpenAQdatasetsLatLng.append(dataset)
  
   
   return ImportOpenAQimported # OpenAQdatasetsLatLng


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

print("  STEP 3 ")

print("********")


print("Getting OpenAQ dataset imported by applying pyOpenAQ API from ") 
print(dt_begin)
print(" to ")
print(dt_end)
print(" for one OpenAQ Station and one parameter ")



# Step 4 Get Measurements from openAQ API 
#
#
# Test 
#
#resp = api.cities(df=True, limit=10000)

#res1 = api.measurements(city='Delhi', df=True, limit=10000)

print("  STEP 4 ")

print("********")

print("Getting Measurements from OpenAQ API source")

ImportedOpenAQimport = Milestone3_Get_Imported_OpenAQ_Dataset()

print("Found these Stations in Coordinates")

OpenAQStationunique = ImportedOpenAQimport['location'].unique()

print(OpenAQStationunique)


#print(Measurements1)

# Step 5 Choose to remove measurement that have -999.00
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


print("  STEP 5 ")

print("********")

print("Choose to remove missing measurements that are -999.0 and below 0")

Remove_Neg = 1 # Edit      Removes Only measurements of -999.0 

Remove_Negative_Measurements = 1 # Edit Remove measure below 0 

Remove_Neg_NO = 0

Remove_Neg_YES = 1

if(Remove_Neg == Remove_Neg_YES):
  ImportedOpenAQimport = Milestone2_Remove_neg_attribute(ImportedOpenAQimport)
  print("Removing missing measurements that are -999.0")
else:
  print("Not removing missing measurements that are -999.0")  
  
if(Remove_Negative_Measurements == Remove_Neg_YES):
  ImportedOpenAQimport = Milestone2_Remove_negative_attribute(ImportedOpenAQimport)
  print("Removing measurement below 0")
  
  
# Step 6 Do Data Wrangling on OpenAQ dataset  
#
# 1 It convert utc to DateTime for Pecos Quality Control and utc to index
#
#   
  

print("  STEP 6 ")

print("********")
  
print("Data Wrangling OpenAQ dataset evaluating UTC date to Date format and setting utc to index")

ImportedOpenAQimport = Milestone2_Get_OpenAQ_Dataset_Wrangling_utc_index(ImportedOpenAQimport)
  

print("Dataset Wrangling Completed")

print("OpenAQ Dataset imported ")

print(ImportedOpenAQimport.dtypes)


# Step 7 Import just Measurements to Dataframe with Date utc index for applying 

print("  STEP 7 ")

print("********")

print("Get measurement to Dataframe")


OpenAQAPIdataset = pd.DataFrame(ImportedOpenAQimport, columns=['value','location'])


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

OpenAQDataset_VisualAnalytics = "OpenAQ Dataset Station " + OpenAQStationdfDatasetCountry + " " + parameter + " Time Schedule " + str(dt_begin) + " to " + str(dt_end)

Milestone2_OpenAQ_Dataset_VisualAnalytics_Histogram_Unique(OpenAQAPIdataset, OpenAQStationunique, OpenAQAPIdataset.index, OpenAQAPIdataset['value'], parameter, OpenAQDataset_VisualAnalytics, xlabel='Value', ylabel='Amount of Measurements', dpi=100)

