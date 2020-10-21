# -*- coding: utf-8 -*-
"""
Created on Mon Oct 19 15:40:07 2020

@author: wegia
"""


import jsonlines
import ndjson
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import pecos

  #      for City in df[Country == df.country].city:    
def Get_OpenAQ_nearestroad_to_location_from_GoogleMaps_RoadAPI(df, lat, lng):
    
    import googlemaps
    
#    pd.Series
    
    print(lat, lng)
    
    Dataset_results = []
    
    Location_info = (lat, lng)
    
    #Location_Attr = pd.DataFrame(Location_info)
    
#    Location_Attr.append(lng)
    
    API = 'AIzaSyARmyW7iU8LGmXgzVb1JWQp0-kJeK1L15E'
    
    print(Location_info)
    
    gmaps = googlemaps.Client(key='AIzaSyARmyW7iU8LGmXgzVb1JWQp0-kJeK1L15E')
    
        
    Results = gmaps.nearest_roads(Location_info)
  
    
  #  Results2 = gmaps.snapped_speed_limits(Location_info)
        
  #  print(Results2)
    
    print(Results)

    print(Results[0]['placeId'])
   
    Dataset_results.append(lat)
    Dataset_results.append(lng)
    # Dataset_results.append(df.location)
    
    
    Dataset_results.append(Results[0]['placeId'])
    
    print(Dataset_results)
    
    return Dataset_results


def Get_OpenAQ_import_nearestroad_to_location_from_GoogleMaps_RoadAPI(df):
    
    iteration = 0
    
    #nextiter = next(df.iterrows())[1]
    
    #print(nextiter)
    
    Dataset_result = []
    
    for index, OpenAQlng in df.iterrows():
  #     print(OpenAQlng['latitude'])
        
       Dataset_results = Get_OpenAQ_nearestroad_to_location_from_GoogleMaps_RoadAPI(df, OpenAQlng['latitude'], OpenAQlng['longitude'])
       
       Dataset_results.append(OpenAQlng['location'])
       Dataset_result.append(Dataset_results) 
 #      print(Dataset_results)
       
       print(OpenAQlng['latitude'],',',OpenAQlng['longitude'],'|')
       
    return Dataset_result
    
def Get_OpenAQ_imports_import_nearestroad_to_location_from_GoogleMaps_RoadAPI(df):


    print(df)

    Dataset10 = []
        
    
   
    Location_Subset = df[['location','latitude','longitude']].copy()

    Parameter_Subset = df[['parameter']].copy()
 
#    Location_Subset = df.location.copy()

 #   Parameter_Subset = df['parameter'].copy()

   # print(len(Location_Subset))

    Location_Subset.sort_values('location', ascending=False)
    Location_Subset = Location_Subset.drop_duplicates(subset='location', keep='first')

    Parameter_Subset.sort_values('parameter', ascending=False) 
    Parameter_Subset = Parameter_Subset.drop_duplicates(subset='parameter', keep='first')

    print(Location_Subset)
    
    for Location in Location_Subset['location']: 
    
        
        #Location_Parameter = df[Location_Subset['location'] == Location]
        
        #print(Location_Parameter)
        
        print(Location)
        
        print(len(Location))           

  

        for Parameter in Parameter_Subset['parameter']:
                    
            Dataset_attr = []
    
            lat = df[Location == df.location].latitude
    
            lng = df[Location == df.location].longitude
    
            lat = lat.drop_duplicates(keep='first')
 
            lat = lat.iloc[0]

            lng = lng.drop_duplicates(keep='first')

            lng = lng.iloc[0]  
   
            Dataset_attr.append(lat)
            Dataset_attr.append(lng)
            Dataset_attr.append(Location)
   #         Dataset_attr.append(Parameter)
            
            Dataset10.append(Dataset_attr)
            #print(Dataset_attr)
            
            print(Dataset10)
            
    Results = pd.DataFrame(Dataset10, columns=['latitude','longitude','location'])
    print(len(Results))
    
    print(Results)
    
    print(Results['latitude'][0])
    print(Results['longitude'][1])
   
    Get_OpenAQ_import_nearestroad_to_location_from_GoogleMaps_RoadAPI(Location_Subset)
    
#    Results.to_csv(r'D:\AirNode\TechnicalStack\AirNode_Dependencies\Functionality\L_IoT\Gatherminer-master\example_data\openAQ_attr.csv',index=False)                       
    return Results                
                    

def Get_OpenAQ_Imported_import_nearestroad_to_location_from_GoogleMaps_RoadAPI(df):
    
    Location_Subset = df[['location']].copy()
 
    print(len(Location_Subset))

    Location_Subset.sort_values('location', ascending=False)
    Location_Subset = Location_Subset.drop_duplicates(subset='location', keep='first')

    Get_OpenAQ_import_nearestroad_to_location_from_GoogleMaps_RoadAPI(df, Location_Subset) 


data_file1 = 'openaq_PM25_copy_3_copy.xlsx';

#df4 = pd.read_csv (r'openAQ_PM25_3_copy_2.csv',index_col=0)


df = pd.read_excel(data_file1, index_col=0)

#Get_OpenAQ_Imported_import_nearestroad_to_location_from_GoogleMaps_RoadAPI(df)

Get_OpenAQ_imports_import_nearestroad_to_location_from_GoogleMaps_RoadAPI(df)


