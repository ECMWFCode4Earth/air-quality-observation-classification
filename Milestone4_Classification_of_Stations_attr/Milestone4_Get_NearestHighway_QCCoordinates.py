# -*- coding: utf-8 -*-
"""
Created on Wed Dec  9 14:10:14 2020

@author: wegia
"""


import pandas as pd

import matplotlib.pyplot as plt

from datetime import datetime, date, time, timezone

import numpy as np

import json

import csv

# Step 1 Initiatlise pyOpenAQ API
#
#  1 There are no edits 

print("  STEP 1 ")

print("********")

print("Initialise pyOpenAQ API")

# api = openaq.OpenAQ()

print("Completed Step 1 ")

print(">")

OpenAQDatasetLatlng = []

OpenAQDatasetNearestHighwayLatlng = []


def Milestone1_Get_OpenAQStation_Latlng(OpenAQStationCountry):
    
   
   OpenAQLatlngDataset = []
 
   try:  
       
     OpenAQLatLng = api.locations(location=OpenAQStationCountry, df=True)
    
     OpenAQLatlngStation = api.locations(df=True) 

     OpenAQDataset = api.locations(location='Dubai', df=True)
   
 #  res1 = api.measurements(coordinates="24.4244,54.43375", parameter=parameter, radius=250000, date_to=dt_end, date_from=dt_begin, df=True, limit=10000)

 #  OpenAQ_Countries = Milestone3_Get_Import_OpenAQ_Countries()

 #  OpenAQStation = Milestone3_Get_Import_OpenAQ_EveryStation(OpenAQ_Countries)


   
     print(OpenAQLatlngStation)

     print(OpenAQDataset.dtypes)
   
  # OpenAQLatLng = OpenAQLatlngStation.query("location==" + str(OpenAQStationCountry) + "")
   
 #  print(OpenAQStation) 
   
     print(OpenAQLatLng)
   
     OpenAQLatlngDataset.append(OpenAQLatLng['coordinates.latitude'])
 
     OpenAQLatlngDataset.append(OpenAQLatLng['coordinates.longitude'])

   except:
       pass


       print("Not Completed ")

   return OpenAQLatlngDataset



def Milestone1_Get_OpenAQStations():
    
    
   ETCDIR = "../../air-quality-observation-classification-ecmwf/etc"
   
   Selector = open(f"{ETCDIR}/all_openaq_locations.json")
   OpenAQlocations = json.loads(Selector.read())
 
   print(OpenAQlocations) 
   
   OpenAQlocation_selector = Milestone1_Get_OpenAQStation_select(OpenAQlocations)    
   
   OpenAQlocation_selectordf = pd.DataFrame(OpenAQlocation_selector, columns=['location','lat','lng','parameters','locations','start_dt','end_dt'])
   
   return OpenAQlocation_selectordf  
    

def Milestone1_Get_OpenAQStation_select(OpenAQlocations):
    
    
    SelectedOpenAQStations = []
    
    for OpenAQSelect in OpenAQlocations:
      
        OpenAQSelection = []
        
        start_dt = datetime.strptime(OpenAQSelect["firstUpdated"], "%Y-%m-%dT%H:%M:%S.%fZ")
        end_dt = datetime.strptime(OpenAQSelect["lastUpdated"], "%Y-%m-%dT%H:%M:%S.%fZ")
     
        
        OpenAQSelection.append(OpenAQSelect['location'])
        OpenAQSelection.append(OpenAQSelect['coordinates']['latitude'])
        OpenAQSelection.append(OpenAQSelect['coordinates']['longitude'])
        OpenAQSelection.append(OpenAQSelect['parameters'])
        OpenAQSelection.append(OpenAQSelect['locations']) 
        OpenAQSelection.append(start_dt)
        OpenAQSelection.append(end_dt)
        
        SelectedOpenAQStations.append(OpenAQSelection) 
   
    
    return SelectedOpenAQStations 

def Milestone3_Get_Import_OpenAQ_EveryStation(OpenAQ_Countries):

   df_DF = [];

   for index, respC in OpenAQ_Countries.iterrows():
    
      df4 = respC.astype("|S")
    
       #   print(df4.dtypes)
    
      print(respC[0])
    
      result1 = api.cities(country=respC[0], df=True, limit=10000)
    
      print(result1)
    
#      result1 = api.locations(country=respC[0], df=True)

       #   print(result1)
    
      for index, res1 in result1.iterrows():
       
         print(res1['city']) 
          
         result = api.locations(city=res1['city'], df=True)

         print(result.dtypes)         
         
         for index1, res2 in result.iterrows():
             
            print(res2)
            
            OpenAQDfDataset = []
            
            OpenAQDfDataset.append(res2['coordinates.latitude'])
            
            OpenAQDfDataset.append(res2['coordinates.latitude'])
           
        #    OpenAQLatlngDataset.append(OpenAQLatLng['coordinates.latitude'])
 
        #    OpenAQLatlngDataset.append(OpenAQLatLng['coordinates.longitude'])
#
            OpenAQDfDataset.append(res2['location'])
 
            df_DF.append(OpenAQDfDataset)
     
           # df_DF.append(res2['location'])
       
     
#   df_7_DF = pd.DataFrame(df_DF)

  # print(len(df_7_DF))
   print(df_DF)

   return df_DF  

    #  print(df_2.astype("|S"))

#       df5 = pd.DataFrame(df5)
       
 #      df7 = df5.to_string()

  #     print(df7)


def Milestone3_Get_Import_OpenAQ_Countries():

   status, resp = api.cities()

   #print(resp)

   resp_attribute = api.countries(df=True)

   df2 = resp_attribute.code

   df3 = pd.DataFrame(df2)

   #print(resp_attribute.code)

#   print(len(df3))

   return df3


def Milestone1_Get_OpnenAQ_Dataset_Measurement_perStation(StationOpenAQCoordinates, Radius, parameter, dt_begin, dt_end):
    
#Step 1 Choose the measurement country to import and parameter 
    
#   res1 = api.measurements(location=StationOpenAQ, parameter=parameter, date_to=dt_end, date_from=dt_begin, limit=10000, df=True)

   measure = ""
  # try: 
   res1 = api.measurements(parameter=parameter, radius=Radius, date_to=dt_end, date_from=dt_begin, df=True, limit=10000)

  # except:
    #   pass
   
   print("Completed measurements ")

   return res1


def Milestone2_Import_OpenAQ_Scatter(Xaxis_Measurement, Yaxis, parameter, title, xlabel, ylabel):
    
   fig, ax = plt.subplots()
   scale = 20.0 
   
   print(Yaxis['DistanceKM'])
   
   ax.scatter(Yaxis['DistanceKM'], Yaxis['Statistics'], c='tab:blue', s=scale, label=parameter, alpha=0.3, edgecolors='none')
   
   ax.legend()
   ax.grid(True)
   plt.gca().set(title=title, xlabel=xlabel, ylabel=ylabel)
   
   plt.show()


def Milestone2_Get_OpenAQStations_unique(OpenAQStations, OpenAQunique):
    
   OpenAQStationsunique = 0
    
   
   iteration = 0
   
   for OpenAQStation in OpenAQStations['locations']:
      
      print(OpenAQStation)
      
      print(OpenAQStations.iloc[iteration])
      
      
      
      iteration = iteration + 1
      
      
      for OpenAQselect in OpenAQStation: 
      
      #   print(OpenAQselect)    
          
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

   
   return ImportOpenAQimported # OpenAQdatasetsLatLng


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
    
   
  # OpenAQStations = Milestone1_Get_OpenAQStations()
   
 #  print(OpenAQStations)
     
   
 
   OpenAQNearestHighway = Milestone4_Get_NearestHighway_OpenAQStations() 
   
  
   for OpenAQunique in OpenAQStationunique:
   
    
      print(OpenAQunique) 
      
      OpenAQAPIdatasetunique = df4[df4['location'] == OpenAQunique]

         
      OpenAQStationLatlng_NearestHighway = Milestone4_Get_NearestHighway_OpenAQStations_OneStation(OpenAQAPIdatasetunique, OpenAQunique, OpenAQNearestHighway)
  
      OpenAQStationLatlng_NearestHighway[1].append(OpenAQAPIdatasetunique['value'].describe()['mean'])
    
      print(OpenAQStationLatlng_NearestHighway)
        
    
      print("Distance to the nearest Highway in Km ")
      
      if(OpenAQStationLatlng_NearestHighway[0] == 1):

         OpenAQStationLatlng_NearestHighway[1].append(OpenAQunique)  
      
   
      if(OpenAQStationLatlng_NearestHighway[0] == 0):
    
         OpenAQStationLatlng_NearestHighway[1].append(0)
         OpenAQStationLatlng_NearestHighway[1].append(0)
         OpenAQStationLatlng_NearestHighway[1].append(0)
         OpenAQStationLatlng_NearestHighway[1].append(0)
         OpenAQStationLatlng_NearestHighway[1].append(0)

         OpenAQStationLatlng_NearestHighway[1].append(0)
      
         OpenAQStationLatlng_NearestHighway[1].append(OpenAQunique)  
      
          
      OpenAQAPIdatasetuniqueDataset.append(OpenAQStationLatlng_NearestHighway[1])
    
      OpenAQDatasetNearestHighwayLatlng.append(OpenAQAPIdatasetunique['value'].describe()['mean'])  
    
      
   OpenAQStationgetlatlng = pd.DataFrame(OpenAQAPIdatasetuniqueDataset, columns=['lat','lng','Place Id','LatitudeNearestHighway','LongitudeNearestHighway','DistanceKM','Statistics','location'])
        
   print("For these OpenAQ Stations")
  
   
   print(OpenAQAPIdatasetuniqueDataset)
   
     
   return OpenAQStationgetlatlng
   

    
def Milestone4_Get_NearestHighway_OpenAQStations_Station(df4, parameter, OpenAQStationunique):
   
   OpenAQAPIdatasetuniqueDataset = [] 
    
     
   
 
   OpenAQNearestHighway = Milestone4_Get_NearestHighway_OpenAQStations() 
   
   OpenAQStations = Milestone1_Get_OpenAQStations()
   
   print(OpenAQStations)
   
   for OpenAQunique in OpenAQStationunique:
        
      print(OpenAQunique) 
      
   #   OpenAQStationLatlng = Milestone1_Get_OpenAQStation_Latlng(OpenAQunique)
  
      OpenAQAPIuniqueDataset = [] 
    
      OpenAQAPIdatasetunique = df4[df4['location'] == OpenAQunique]
     
      OpenAQStationLatlng = OpenAQStations[OpenAQStations['location'] == OpenAQunique]  
      
     
      
      if(len(OpenAQStationLatlng) == 0):
        
      #  OpenAQStationLatlng = Milestone2_Get_OpenAQStations_unique(OpenAQStations, OpenAQunique)  
          
      # OpenAQStationLatlng = OpenAQStations[OpenAQStations['location'] == OpenAQunique] 
        
        
     #   iteration = 0
        
      #  for OpenAQStationAlt in OpenAQStations:
            
          # if(OpenAQStationAlt == OpenAQunique):
               
        
      #     OpenAQStationLatlng = OpenAQStations[OpenAQStations['locations'][iteration] == OpenAQunique]           
      
        
        
       #    iteration = iteration + 1 
        
       print(OpenAQStationLatlng)
      
       OpenAQStationLatlng_NearestHighway = Milestone4_Get_NearestHighway_OpenAQStations_OneStation(OpenAQStationLatlng, OpenAQunique, OpenAQNearestHighway)

       print(OpenAQAPIdatasetunique['value'].describe())

       print("Distance to the nearest Highway in Km ")
      
       if(OpenAQStationLatlng_NearestHighway[0] == 1):

         OpenAQAPIuniqueDataset.append(OpenAQStationLatlng_NearestHighway[1])
         OpenAQAPIuniqueDataset.append(OpenAQStationLatlng_NearestHighway[2])
         OpenAQAPIuniqueDataset.append(OpenAQStationLatlng_NearestHighway[3])
  
         if(len(OpenAQStationLatlng_NearestHighway[4]) == 6):
        #   print(OpenAQStationLatlng_NearestHighway[4][5])
           
           OpenAQDatasetNearestHighwayLatlng.append(OpenAQStationLatlng_NearestHighway[4][5])
          
           OpenAQAPIuniqueDataset.append(OpenAQStationLatlng_NearestHighway[4][5])
         else:
           OpenAQAPIuniqueDataset.append(0)
          
           OpenAQDatasetNearestHighwayLatlng.append(0)

       if(OpenAQStationLatlng_NearestHighway[0] == 0):
    
         OpenAQAPIuniqueDataset.append(0)
         OpenAQAPIuniqueDataset.append(0)
         OpenAQAPIuniqueDataset.append(0)

         OpenAQAPIuniqueDataset.append(0)
      
        
       OpenAQDatasetNearestHighwayLatlng.append(OpenAQAPIdatasetunique['value'].describe()['mean'])  
       OpenAQAPIuniqueDataset.append(OpenAQAPIdatasetunique['value'].describe()['mean'])
      
       OpenAQAPIdatasetuniqueDataset.append(OpenAQAPIuniqueDataset)
      
      
   print("For these OpenAQ Stations")
  
   print(OpenAQAPIuniqueDataset)
   
   print(OpenAQAPIdatasetuniqueDataset)
   
     
   return OpenAQAPIdatasetuniqueDataset
   

   
OpenAQ_Dataset_LatlngCSV_Download = 'OpenAQ_Dataset Unique selection pm25 CoordinateCentreandRadius 2020-03-01 to 2020-09-01.csv'
 
OpenAQAPIdataset = Milestone3_Get_Imported_OpenAQ_Dataset(OpenAQ_Dataset_LatlngCSV_Download)

print("  STEP 1 ")

print("********")

print("Get Distance to Nearest Highway")

parameter = 'pm25'

print("Distance to the nearest Highway in Km ")


OpenAQStationunique = OpenAQAPIdataset['location'].unique()

print(OpenAQStationunique)

#OpenAQlatStations = Milestone1_Get_OpenAQStations()

# print(OpenAQlatStations)

OpenAQStationsdatasetmeasurements = Milestone4_Get_NearestHighway_OpenAQStations_QCalt_Station(OpenAQAPIdataset, parameter, OpenAQStationunique)

# OpenAQStationsdatasetmeasurements = pd.DataFrame(OpenAQStationsdatasetmeasurements, columns=['location','lat','lng','NearestHighway','location','Statistics'])

title="Distance Nearest Highway"
   
xlabel='Distance to Nearest Highway in Km'
   
ylabel='Mean of Measurements'
   
Milestone2_Import_OpenAQ_Scatter(OpenAQStationunique, OpenAQStationsdatasetmeasurements, parameter, title, xlabel, ylabel)
   
print("Found these Stations in selection")

print(OpenAQStationunique)

# Step 4 Visual Analytics of OpenAQ Dataset 
#
# Visual Analytics for Every Station or not
#
#  Change VisualAnalytics_Complete = 1 
#
#  1 - Every station 
#
#  0 - Only one histogram for OpenAQ Dataset

VisualAnalytics_Complete = 1

# Step 5 When OpenAQ API fails add Station failed on and retry
#
# 1 Change the variable to next number of statation after last completed 
#
# 2 Change Completed_QC_Processes 
#
# i.e. when 3 report completed change to 4 

Completed_QC_Processes = 0

# OpenAQNearestHighway = Milestone4_Get_NearestHighway_OpenAQStations()

print("Get Distance to Nearest Highway")


print("Distance to the nearest Highway in Km ")

title="Distance Nearest Highway"
   
xlabel='Distance to Nearest Highway in Km'
   
ylabel='Mean of Measurements'
   
