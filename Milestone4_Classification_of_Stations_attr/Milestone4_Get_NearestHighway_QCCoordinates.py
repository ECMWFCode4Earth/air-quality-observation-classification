# -*- coding: utf-8 -*-
"""
Created on Wed Dec  9 14:10:14 2020

@author: wegia
"""


import pandas as pd

import matplotlib.pyplot as plt

from datetime import datetime, date, time, timezone

import numpy as np

import csv


OpenAQDatasetLatlng = []

OpenAQDatasetNearestHighwayLatlng = []

def Milestone2_Import_OpenAQ_Scatter_many(OpenAQdatasetlatlngunique, parameter, title, xlabel, ylabel):
   
    if(len(parameter) > 0):

        
       print(type(OpenAQdatasetlatlngunique[0]))
       
       
       Milestone2_Import_OpenAQ_Scatter(OpenAQdatasetlatlngunique[0]['DistanceKM'], OpenAQdatasetlatlngunique[0]['Statistics'], parameter[0], title, xlabel, ylabel)
     
    if(len(parameter) == 0):
    
       for OpenAQStationparameter in OpenAQdatasetlatlngunique:
       
          print(OpenAQStationparameter)    
         
          OpenAQStation = title + " " + OpenAQStationparameter['location'] + OpenAQStationparameter['parameter']    
          
          Milestone2_Import_OpenAQ_Scatter(OpenAQStationparameter['DistanceKM'], OpenAQStationparameter['Statistics'], OpenAQStationparameter['parameter'], OpenAQStation, xlabel, ylabel)
      
        

def Milestone2_Import_OpenAQ_Scatter(Xaxis_Measurement, Yaxis, parameter, title, xlabel, ylabel):
    
   fig, ax = plt.subplots()
   scale = 20.0 
   
   print(Yaxis)
   
   ax.scatter(Xaxis_Measurement, Yaxis, c='tab:blue', s=scale, label=parameter, alpha=0.3, edgecolors='none')
   
   ax.legend()
   ax.grid(True)
 #  plt.gca().set(title=title, xlabel=xlabel, ylabel=ylabel)
   
   plt.show()


def Milestone2_Get_OpenAQStations_unique(OpenAQStations, OpenAQunique):
    
   OpenAQStationsunique = 0
    
   
   iteration = 0
   
   for OpenAQStation in OpenAQStations['locations']:
      
      print(OpenAQStation)
      
      print(OpenAQStations.iloc[iteration])
    
      iteration = iteration + 1
   
      for OpenAQselect in OpenAQStation: 
      
         if(str(OpenAQselect) == str(OpenAQunique)):  
            
           OpenAQStationsunique = OpenAQselect  
    
           OpenAQgetStationunique = OpenAQStations.iloc[iteration]
           
           print(OpenAQgetStationunique)
    
           print(OpenAQStationsunique)
           
           break
           
      OpenAQStationsunique.append(OpenAQStation)
    
   return OpenAQStationsunique

def Milestone3_Get_Imported_OpenAQ_Dataset(OpenAQ_Dataset_LatlngCSV_Download): 
    
   OpenAQ_Dataset_LatlngCSV_Download = "../Milestone1_Importing-datasets-from-OpenAQ/" + OpenAQ_Dataset_LatlngCSV_Download
   
   
  # OpenAQ_Dataset Unique selection pm25 CoordinateCentreandRadius 2020-03-01 to 2020-09-01.csv" # 

 
   ImportOpenAQimported = pd.read_csv(OpenAQ_Dataset_LatlngCSV_Download)

   
   return ImportOpenAQimported 


def Milestone4_Get_NearestHighway_OpenAQStations_OneStation(OpenAQLatlng, OpenAQunique, OpenAQdatasetsLatLng):
  
 
   OpenAQgetStationlatlngdataset = []
   
   print(OpenAQLatlng.iloc[0]['coordinates.latitude'])
   
   OpenAQgetStationlatlngdataset.append(0)
      
   print(OpenAQLatlng.iloc[0]['coordinates.latitude'].round(decimals=4))
   
   for OpenAQStationLatlng in OpenAQdatasetsLatLng[0]:
   
     
     OpenAQStationDatasetLatlng = OpenAQStationLatlng.split('?')
    
     OpenAQStationDatasetLatlng[0] = float(OpenAQStationDatasetLatlng[0])
     
     OpenAQStationDatasetLatlng[1] = float(OpenAQStationDatasetLatlng[1])
     
     if(float(OpenAQStationDatasetLatlng[0]) == float(OpenAQLatlng.iloc[0]['coordinates.latitude'])):
         
        print(OpenAQStationDatasetLatlng[0])
    
        OpenAQgetStationlatlngdataset[0] = 1
    
        OpenAQgetStationlatlngdataset.append(OpenAQStationDatasetLatlng)
   
     else: 
     
        if(round(OpenAQStationDatasetLatlng[0],4) == (OpenAQLatlng.iloc[0]['coordinates.latitude'].round(decimals=4))):
    
          print(OpenAQStationDatasetLatlng[0])
    
          OpenAQgetStationlatlngdataset[0] = 1
    
          OpenAQgetStationlatlngdataset.append(OpenAQStationDatasetLatlng)
       
   return OpenAQgetStationlatlngdataset

def Milestone4_Get_Statistics_parameters(df4, OpenAQdatasetunique):
    
    OpenAQparameterunique = df4['parameter'].unique()

    OpenAQStationLatlngparameter = []

    OpenAQStationLatlng_NearestHighway = []

    print(OpenAQparameterunique)

    for OpenAQStationparameter in OpenAQparameterunique:
 
       OpenAQStationLatlng = []
    
       OpenAQdatasetlatlngunique = df4[df4['parameter'] == OpenAQStationparameter]
      
       OpenAQDatasetNearestHighwayLatlng = Milestone4_Get_NearestHighway_OpenAQStations_QCalt_Station(OpenAQdatasetlatlngunique, OpenAQStationparameter, OpenAQStationunique)
    
     #  OpenAQDatasetNearestHighwayLatlng.append(OpenAQStationLatlngparameter)
  
       OpenAQStationLatlngparameter.append(OpenAQStationLatlngparameter)
       
   #    OpenAQDatasetNearestHighwayLatlng.append(OpenAQdatasetlatlngunique['value'].describe()['mean'])
   
   #    OpenAQDatasetNearestHighwayLatlng.append(OpenAQStationLatlng)     
   
   #    OpenAQStationLatlng.append(OpenAQdatasetlatlngunique['value'].describe())
   
       OpenAQStationgetlatlng = pd.DataFrame(OpenAQDatasetNearestHighwayLatlng, columns=['lat','lng','Place Id','LatitudeNearestHighway','LongitudeNearestHighway','DistanceKM','location','parameter','Statistics'])
       
       OpenAQStationLatlng_NearestHighway.append(OpenAQStationgetlatlng)                                                                                  
       
       
       title="Distance Nearest Highway " + OpenAQStationgetlatlng['location'] 
   
       xlabel='Distance to Nearest Highway in Km'
   
       ylabel='Mean of Measurements'
       
       Milestone2_Import_OpenAQ_Scatter(OpenAQStationgetlatlng['DistanceKM'], OpenAQStationgetlatlng['Statistics'], OpenAQStationparameter, title, xlabel, ylabel)
       
       
   # OpenAQStationLatlng_NearestHighway = pd.DataFrame(OpenAQStationLatlng_NearestHighway,columns=OpenAQStationLatlngparameter)
   
    
    return OpenAQStationLatlng_NearestHighway

def Milestone4_Get_NearestHighway_OpenAQStations():
  
   OpenAQ_Dataset_LatlngCSV_Download = "openAQ_copy100Latlngattr13000_OpenAQStations.csv"
   
   
   OpenAQdatasetsLatLng = []
   
   delimiterOpenAQ = ','
   with open(OpenAQ_Dataset_LatlngCSV_Download,'r') as dest_f:
    data_iter = csv.reader(dest_f, delimiter=delimiterOpenAQ)
    
    for dataset in data_iter:
       OpenAQdatasetsLatLng.append(dataset)

   
   return OpenAQdatasetsLatLng


def Milestone4_Get_NearestHighway_OpenAQStations_QCalt_Station(df4, parameter, OpenAQStationunique):
 
   OpenAQAPIdatasetuniqueDataset = [] 
    
     
 
   OpenAQNearestHighway = Milestone4_Get_NearestHighway_OpenAQStations() 
   
  
   for OpenAQunique in OpenAQStationunique:
   
    
      print(OpenAQunique) 
      
      OpenAQAPIdatasetunique = df4[df4['location'] == OpenAQunique]

         
      OpenAQStationLatlng_NearestHighway = Milestone4_Get_NearestHighway_OpenAQStations_OneStation(OpenAQAPIdatasetunique, OpenAQunique, OpenAQNearestHighway)
  
    
      print(OpenAQStationLatlng_NearestHighway)
        
    
      print("Distance to the nearest Highway in Km ")
      
      if(OpenAQStationLatlng_NearestHighway[0] == 1):


         if(len(OpenAQStationLatlng_NearestHighway[1]) != 6):
         
             
           OpenAQStation = 6 - len(OpenAQStationLatlng_NearestHighway[1])
           
           if(OpenAQStation == 2):
           
              OpenAQStationLatlng_NearestHighway[1].append(0) 
              OpenAQStationLatlng_NearestHighway[1].append(0)
          
           if(OpenAQStation == 3):
               
              OpenAQStationLatlng_NearestHighway[1].append(0) 
              OpenAQStationLatlng_NearestHighway[1].append(0) 
              OpenAQStationLatlng_NearestHighway[1].append(0)   
   
           if(OpenAQStation == 4):
               
              OpenAQStationLatlng_NearestHighway[1].append(0)
              OpenAQStationLatlng_NearestHighway[1].append(0)   
              OpenAQStationLatlng_NearestHighway[1].append(0)
              OpenAQStationLatlng_NearestHighway[1].append(0)


         OpenAQStationLatlng_NearestHighway[1].append(OpenAQunique)  
      
         OpenAQStationLatlng_NearestHighway[1].append(parameter)
           
      
         if(len(OpenAQAPIdatasetunique) == 0):
      
            OpenAQStationLatlng_NearestHighway[1].append(0)
      
         else: 
      
            OpenAQStationLatlng_NearestHighway[1].append(OpenAQAPIdatasetunique['value'].describe()['mean'])  
    
            OpenAQAPIdatasetuniqueDataset.append(OpenAQStationLatlng_NearestHighway[1])
       
      
    
   
      if(OpenAQStationLatlng_NearestHighway[0] == 0):
    
         OpenAQStationLatlng_NearestHighway[1].append(0)
         OpenAQStationLatlng_NearestHighway[1].append(0)
         OpenAQStationLatlng_NearestHighway[1].append(0)
         OpenAQStationLatlng_NearestHighway[1].append(0)
         OpenAQStationLatlng_NearestHighway[1].append(0)

         OpenAQStationLatlng_NearestHighway[1].append(OpenAQunique)  
 
    
         
   print("For these OpenAQ Stations")
  
   
   print(OpenAQAPIdatasetuniqueDataset)
   
   return OpenAQAPIdatasetuniqueDataset
   

print("  STEP 1 ")

print("********")

OpenAQ_Dataset_LatlngCSV_Download = 'OpenAQ_Dataset Unique selection Radius 25000 pm25 Selection 2020-03-01 to 2020-09-01.csv'


# 'OpenAQ_Dataset Unique selection pm25 CoordinateCentreandRadius 2020-03-01 to 2020-09-01.csv'
 
OpenAQAPIdataset = Milestone3_Get_Imported_OpenAQ_Dataset(OpenAQ_Dataset_LatlngCSV_Download)

## Step 2 
##
## Choose on parameter or every


print("  STEP 2 ")

print("********")

print("Get Distance to Nearest Highway")

parameter = 'pm25'

Onlyoneparameter = 0 # Edit 1 Only one parameter 0 parameter from OpenAQ station

parameter_selection = []

if(Onlyoneparameter == 1):
  
  parameter_selection.append(parameter)

  
print("  STEP 3 ")

print("********")

print("Distance to the nearest Highway for these OpenAQ stations in Km ")

OpenAQStationunique = OpenAQAPIdataset['location'].unique()

print(OpenAQStationunique)

print("  STEP 4 ")

print("********")

OpenAQStationsdatasetmeasurements = Milestone4_Get_Statistics_parameters(OpenAQAPIdataset, OpenAQStationunique)

print("Found these Statitics ")

print(OpenAQStationsdatasetmeasurements)

print("  STEP 5 ")

print("********")

print("Scatter plot of Nearest Highway to Mean for OpenAQ stations ")

title="Distance Nearest Highway"
   
xlabel='Distance to Nearest Highway in Km'
   
ylabel='Mean of Measurements'
   
Milestone2_Import_OpenAQ_Scatter_many(OpenAQStationsdatasetmeasurements, parameter_selection, title, xlabel, ylabel)
   
print("Found these Stations in selection")

print(OpenAQStationunique)

