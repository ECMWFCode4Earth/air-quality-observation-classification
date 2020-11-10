# -*- coding: utf-8 -*-
"""
Created on Mon Nov  9 11:29:05 2020

@author: wegia
"""


import googlemaps
from datetime import datetime
import pandas as pd

import csv

from math import sin, cos, sqrt, atan2, radians

def Get_latLngopenAQ():
    
#
    df = pd.DataFrame()
     
    df_2 = []
    
    with open('Latlng2openAQ1.csv', 'r') as f:
        reader = csv.reader(f, delimiter="|")
        for row in reader:
         #  print(row)
               
           for e in row:
           
              df_latlng = e.split(',')
    
           #   print(df_latlng) 
              df_2.append(df_latlng)
 
    return df_2    


def Get_latLng2openAQ():
    

    df = pd.DataFrame()
     
    df_2 = []
    
    with open('Latlng2openAQ1.csv', 'r') as f:
        reader = csv.reader(f, delimiter="|")
        for row in reader:
         #  print(row)
               
           for e in row:
           
              df_latlng = e.split(',')
    
              print(df_latlng) 
              df_2.append(df_latlng)
 
 
    return df_2    

def Get_OpenAQ_nearestroad_openAQ_to_location_from_GoogleMaps_RoadAPI(latlngstations, ResultsDataset):
  
  
    for latlng in latlngstations:
    

       Results = Get_OpenAQ_nearestroad_to_location_from_GoogleMaps_RoadAPI(latlng[0], latlng[1]) 
    
       ResultsDataset.append(Results)
    
    return ResultsDataset


def Get_Distance_stationsTwoLatLng(Dataset_Results):
    
    
   for latlngstations in Dataset_Results: 

      print(latlngstations)  
       
      if(len(latlngstations) > 3): 
  
        OpenAQ_lat = latlngstations[0]
       
        OpenAQ_lng = latlngstations[1]
       
        NearestHighway_lat = latlngstations[3]
       
        NearestHuighway_lng = latlngstations[4]
  
        Results1 = Get_Distance_TwoLatLng(OpenAQ_lat, OpenAQ_lng, NearestHighway_lat, NearestHuighway_lng)

        latlngstations.append(Results1)   


   return Dataset_Results


def Get_OpenAQ_nearestroad_to_location_from_GoogleMaps_RoadAPI(lat, lng):
    
    import googlemaps
    
    
    Dataset_results = []
    
    Location_info = (lat, lng)
    
  
    Results = gmaps.nearest_roads(Location_info)
  
    
   
    Dataset_results.append(lat)
    Dataset_results.append(lng)
    
    
    if(len(Results) != 0):
      Dataset_results.append(Results[0]['placeId'])
  
    
    return Dataset_results


        
def Get_OpenAQ_latlng(openAQattr):
   
   df = pd.DataFrame()
    
   
   
   
   for res1 in openAQattr:
   
      print(res1)   
         
      print("Latlng")
      
   return df

def Get_Distance_TwoLatLng(OpenAQ_lat, OpenAQ_lng, NearestHighway_lat, NearestHuighway_lng):

   # Step 1 approximate radius of earth in km
   R = 6373.0

   print(OpenAQ_lat)
   
   lat1 = radians(float(OpenAQ_lat))
   lon1 = radians(float(OpenAQ_lng))
   lat2 = radians(float(NearestHighway_lat))
   lon2 = radians(float(NearestHuighway_lng))


#Step 2 Get nearest Highway Distance 
   
   dlon = lon2 - lon1
   dlat = lat2 - lat1

   a = sin(dlat / 2)**2 + cos(lat1) * cos(lat2) * sin(dlon / 2)**2
   c = 2 * atan2(sqrt(a), sqrt(1 - a))

#Step 3 R * C
  
   distance = R * c

   print("Result:", distance)
 

   return distance

def Get_stationPlaceIdlatlng(Results_Datasets):
    
   
 #  placeId = gmaps.place('ChIJVYBZP-Oxj4ARls-qJ_G3tgM')

   print(Results_Datasets) 
   
   try:
    # block raising an exception
    placeId = gmaps.place(Results_Datasets)

   except:
    pass # doing nothing on exception 
    placeId = 0
    
   print(placeId)

   return placeId


def Get_Stations_PlaceIdlatlng(Results_Dataset):
  
   for latlngstations in Results_Dataset:
  
         
      if(len(latlngstations) > 2):
      
        Results = Get_stationPlaceIdlatlng(latlngstations[2])
    
        if(Results != 0):
  
          OpenAQ_lat = Results['result']['geometry']['location']['lat']

          OpenAQ_lng = Results['result']['geometry']['location']['lng']
      
          latlngstations.append(OpenAQ_lat)
          
          latlngstations.append(OpenAQ_lng)
          
   return Results_Dataset 
    
    
print("Getting Lat lng and distance")


def Test_GetdistanceLatlngStation():


#Step 2 Use placeId to get lat lng 

   placeId = gmaps.place('ChIJVYBZP-Oxj4ARls-qJ_G3tgM')

#print(placeId)

   print("Longitude")

   print(placeId['result']['geometry']['location']['lng'])

   print("Latitude")
   print(placeId['result']['geometry']['location']['lat'])

#Step 3 Get Lat lng station

   OpenAQ_lat = placeId['result']['geometry']['location']['lat']
   OpenAQ_lng = placeId['result']['geometry']['location']['lng']

   NearestHighway_lat = 0 
   NearestHighway_lng = 0

#Step 4 Get neareest Highway distance
      
   Res1 = Get_Distance_TwoLatLng(OpenAQ_lat, OpenAQ_lng, NearestHighway_lat, NearestHuighway_lng)
 
   print(Res1)

def Test_Outputting_Df_csv():
    
   Res2 = []

   Res = 0

   df = pd.DataFrame()

   df.append(Res2)

   # change when new process
   
   df.to_csv("results_res1.csv")

   Res = 1

   return Res

def Test_Get_Distance_TwoLatLng(OpenAQ_lat, OpenAQ_lng, NearestHighway_lat, NearestHuighway_lng):

   # approximate radius of earth in km
   R = 6373.0

   lat1 = radians(OpenAQ_lat)
   lon1 = radians(OpenAQ_lng)
   lat2 = radians(52.406374)
   lon2 = radians(16.9251681)

   dlon = lon2 - lon1
   dlat = lat2 - lat1

   a = sin(dlat / 2)**2 + cos(lat1) * cos(lat2) * sin(dlon / 2)**2
   c = 2 * atan2(sqrt(a), sqrt(1 - a))

   distance = R * c

   print("Result:", distance)
   print("Should be:", 278.546, "km")

   return distance

#Step 1 Get Lat lng from openAQ stations from csv
   

OpenAQ_stationlatlng = Get_latLngopenAQ()


#Step 2 Choose the API 

gmaps = googlemaps.Client(key='')

#Step 3 Get nearest highway placeId 

ResultsDataset = []

ResultsDataset = Get_OpenAQ_nearestroad_openAQ_to_location_from_GoogleMaps_RoadAPI(OpenAQ_stationlatlng, ResultsDataset)


#Step 4 Output to csv 


def Get_Output_Latlng_csv(ResultsDataset):
   
   for Results_1Dataset in ResultsDataset:
    
      dfres = pd.DataFrame()

      dfres.append(Results_1Dataset)
      
      dfres.to_csv(r'openAQ_adding1_2Latlngattr1000_test.csv',index=False)    

Get_Output_Latlng_csv(ResultsDataset)

#Step 5 Use placeId to get lat lng 

ResultsDataset = Get_Stations_PlaceIdlatlng(ResultsDataset)


#Step 6 Get distance to Nearest Highway 
#
# It uses Get_Distance_TwoLatLng(OpenAQ_lat, OpenAQ_lng, NearestHighway_lat, NearestHuighway_lng)

df_7_DF = Get_Distance_stationsTwoLatLng(ResultsDataset)

dfres1 = pd.DataFrame()

dfres1.append(df_7_DF)

#Step 7 Output to csv 

def Get_LatlngRes(Result_Dataset): 

   for df1 in Result_Dataset: 
   
      dfres1 = pd.DataFrame()

      dfres1.append(df1)

      dfres1.to_csv(r'openAQ_100Latlngattr100_test.csv',index=False)    

Get_LatlngRes(df_7_DF)
