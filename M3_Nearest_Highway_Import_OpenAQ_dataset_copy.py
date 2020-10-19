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
def Get_OpenAQ_nearestroad_to_location_from_GoogleMaps_RoadAPI(lat, lng):
    
    import googlemaps
    
#    pd.Series
    
    Location_info = (lat, lng)
    
    #Location_Attr = pd.DataFrame(Location_info)
    
#    Location_Attr.append(lng)
    
    API = ''
    
    print(Location_info)
    
    gmaps = googlemaps.Client(key=API)
    
        
    Results = gmaps.nearest_roads(Location_info)
  
  #  Results2 = gmaps.snapped_speed_limits(Location_info)
        
  #  print(Results2)
    
    print(Results)
    
    return Results


def Get_OpenAQ_import_nearestroad_to_location_from_GoogleMaps_RoadAPI(df):
    
    for df4 in df:
        
        lat = df4['latitude']
        
        lng = df4['longitude']
        
        Get_OpenAQ_nearestroad_to_location_from_GoogleMaps_RoadAPI(lat, lng)
    

def Get_OpenAQ_Imported_import_nearestroad_to_location_from_GoogleMaps_RoadAPI(df):
    
    Location_Subset = df[['location']].copy()
 
    print(len(Location_Subset))

    Location_Subset.sort_values('location', ascending=False)
    Location_Subset = Location_Subset.drop_duplicates(subset='location', keep='first')

    Get_OpenAQ_import_nearestroad_to_location_from_GoogleMaps_RoadAPI(Location_Subset) 


data_file1 = 'openAQ_PM25_3_copy.xlsx';

#df4 = pd.read_csv (r'openAQ_PM25_3_copy_2.csv',index_col=0)


df = pd.read_excel(data_file1, index_col=0)

Get_OpenAQ_Imported_import_nearestroad_to_location_from_GoogleMaps_RoadAPI(df)
