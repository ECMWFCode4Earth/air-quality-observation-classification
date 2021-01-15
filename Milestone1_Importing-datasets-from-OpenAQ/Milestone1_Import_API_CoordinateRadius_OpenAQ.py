# -*- coding: utf-8 -*-
"""
Created on Tue Dec  8 12:13:31 2020

@author: wegia
"""



import openaq

import pandas as pd

from pandas import json_normalize

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

def Milestone1_Get_OpnenAQ_Dataset_Measurement_perStation(StationOpenAQCoordinates, Radius, parameter, dt_begin, dt_end):
    
#Step 1 Choose the measurement coordinate centre radius to import and parameter 
   
   if(len(parameter) == 1):
       
      res1 = api.measurements(coordinates=StationOpenAQCoordinates, parameter=parameter[0], radius=Radius, date_to=dt_end, date_from=dt_begin, df=True, limit=10000)
  
   else:  
   
      res1 = api.measurements(coordinates=StationOpenAQCoordinates, radius=Radius, date_to=dt_end, date_from=dt_begin, df=True, limit=10000)
      
   
   print("Completed measurements ")

   return res1



def Milestone1_Get_Measurements_CSV_OpenAQStation(OpenAQ_Stations, SelectionOpenAQChoose, parameter, SelectionOpenAQ, dt_begin, dt_end):
    
   OpenAQDataset = r'OpenAQ_Dataset'
 
   SelectedOpenAQ = "Selection"
   
   if(SelectionOpenAQ == 0):
     SelectedOpenAQ = "One Station"
      
   if(SelectionOpenAQ == 1):
     SelectedOpenAQ = "CoordinateCentreandRadius"
  
   if(SelectionOpenAQ == 2):
     SelectedOpenAQ = "Country"
   
    
   OpenAQDataset = OpenAQDataset + " " + SelectionOpenAQChoose + " " + parameter + " " + SelectedOpenAQ + " " +  str(dt_begin) + " to " + str(dt_end) + ".csv" 
    
   print("Printed OpenAQ import to ")
   
   print( OpenAQDataset)
   
   OpenAQ_Stations.to_csv(OpenAQDataset,index=False)                       


def Milestone1_Print_CSV_OpenAQ_Import(OpenAQ_Dataset):

   OpenAQ_Dataset_Import = "OpenAQ_Dataset"
    
   OpenAQ_DatasetCSV = "r'" + OpenAQ_Dataset_Import +  ".csv'" 
    
   OpenAQ_Dataset.to_csv(OpenAQ_DatasetCSV,index=False)                       



print("Get the OpenAQ measurements for stations within raduis of chosen Coordinates from OpenAQ and doing Quality Control on it")

#Step 2 Choose the measurement coordinates and Radius to import and parameter
#
# Choose the coordinates latitude, longitude and Radius
#
# OpenAQStationCoordinates = ''
#
# Radius = ''  in metres

print("  STEP 2 ")

print("********")

print("Chosen OpenAQ Coordinates Lat/lng and Radius: ")
    
 
     
OpenAQStationCoordinates = "-34.60638,-58.43194" #Edit Lat, Lng

Radius = 25000 # Edit in metres 

print(OpenAQStationCoordinates)

print(Radius)

print("Completed Step 2 ")

print(">")

# Step 3 Choose parameter
#
# 1 Choose to import one parameter or all parameters for OpenAQ Station
#
#
# Change to 1 All OpenAQ parameters or 0 - One parameter and select it
#
# Change parameter = '' to selected


print("  STEP 3 ")

print("********")

SelectEveryParameter_YesorNo = 1 # Edit 1 Yes 0 No just one 

parameter = 'pm25'  # Edit

parameter_selection = []

print("Parameter chosen")

if(SelectEveryParameter_YesorNo == 0):
    
   parameter_selection.append(parameter)

   print(parameter_selection)

if(SelectEveryParameter_YesorNo == 1):
    
   print("Every parameter at selected or chosen OpenAQ station") 



print("Completed Step 3 ")

print(">")


#Step 4 Choose time schedule 
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

print("  STEP 4 ")

print("********")


print("Getting OpenAQ dataset applying pyOpenAQ API from ") 
print(dt_begin)
print(" to ")
print(dt_end)
print(" for one OpenAQ Station and one parameter ")




print("Completed Step 4 ")

print(">")


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

res2 = Milestone1_Get_OpnenAQ_Dataset_Measurement_perStation(OpenAQStationCoordinates, Radius, parameter_selection, dt_begin, dt_end)

print("Found these Stations in Coordinates")

OpenAQStationunique = res2['location'].unique()

print(OpenAQStationunique)

print("Completed Step 5 ")

print(">")

# Step 6 Get Measurements CSV
#  
#  Choose unique selection 
#
#  Change   SelectionOpenAQChoose = " "


print("  STEP 6 ")

print("********")

print("Getting Measurements to CSV ")

SelectionOpenAQ = 1

SelectionOpenAQChoose = "Unique selection 24.4244 54.43375"

Milestone1_Get_Measurements_CSV_OpenAQStation(res2, SelectionOpenAQChoose, parameter, SelectionOpenAQ, dt_begin, dt_end)


print("Completed Step 6 ")

print(">")
