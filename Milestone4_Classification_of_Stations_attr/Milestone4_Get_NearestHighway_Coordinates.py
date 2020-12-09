# -*- coding: utf-8 -*-
"""
Created on Wed Dec  9 14:10:14 2020

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

   res1 = api.measurements(parameter=parameter, radius=Radius, date_to=dt_end, date_from=dt_begin, df=True, limit=10000)

   print("Completed measurements ")

   return res1


def Milestone2_Import_OpenAQ_Scatter(Xaxis_Measurement, Yaxis, parameter, title, xlabel, ylabel):
    
   fig, ax = plt.subplots()
   scale = 200.0 
   ax.scatter(Xaxis_Measurement, Yaxis, c='tab:blue', s=scale, label=parameter, alpha=0.3, edgecolors='none')
   
   ax.legend()
   ax.grid(True)
   plt.gca().set(title=title, xlabel=xlabel, ylabel=ylabel)
   
   plt.show()


def Milestone3_Get_Imported_OpenAQ_Dataset(): 
    
   OpenAQ_Dataset_LatlngCSV_Download = 'OpenAQ_DatasetUniquepm25CoordinateCentreandRadius2020-03-01to2020-09-01.csv'

   df = pd.read_csv('OpenAQ_Dataset1pm25Country2020-03-01to2020-09-01.csv')
   
   
   
   print(df['value'])
   
   OpenAQdatasetsLatLng = []
   ImportOpenAQimported = pd.read_csv(OpenAQ_Dataset_LatlngCSV_Download)
    
   print(ImportOpenAQimported['parameter'])
   delimiterOpenAQ = ' '
   with open(OpenAQ_Dataset_LatlngCSV_Download,'r') as dest_f:
       
    print(dest_f)
    
    
    print(ImportOpenAQimported)
    
    data_iter = csv.reader(dest_f, delimiter=delimiterOpenAQ)
    
    for dataset in data_iter:
       OpenAQdatasetsLatLng.append(dataset)
   #    print(dataset)
       
  #  OpenAQDataset = np.asarray(OpenAQdatasetsLatLng)
   
   
   return ImportOpenAQimported # OpenAQdatasetsLatLng


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
   
   
OpenAQAPIdataset = Milestone3_Get_Imported_OpenAQ_Dataset()

print("  STEP 1 ")

print("********")

print("Get Distance to Nearest Highway")

parameter = 'pm25'

# OpenAQStationLatlng = Milestone1_Get_OpenAQStation_Latlng(OpenAQStationCountry)

# OpenAQStationLatlng_NearestHighway = Milestone4_Get_NearestHighway_OpenAQStations(OpenAQStationLatlng)

# print(OpenAQAPIdataset['value'].describe())

print("Distance to the nearest Highway in Km ")

# print(OpenAQStationLatlng_NearestHighway[4])


OpenAQStationunique = OpenAQAPIdataset['location'].unique()

Milestone4_Get_NearestHighway_OpenAQStations_Station(OpenAQAPIdataset, parameter, OpenAQStationunique)

