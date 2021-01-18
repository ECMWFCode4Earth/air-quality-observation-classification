# -*- coding: utf-8 -*-
"""
Created on Tue Dec  8 12:13:31 2020

@author: wegia
"""



import openaq

import pandas as pd

from pandas import json_normalize

from datetime import datetime, date, time, timezone

import time

import numpy as np

import csv


MAX_RETRIES = 10

RetriesPassed_YesNo = 1

# Step 1 Initiatlise pyOpenAQ API
#
#  1 There are no edits 

print("  STEP 1 ")

print("********")

print("Initialise pyOpenAQ API")

api = openaq.OpenAQ()


print("OpenAQ pyOpenAPI begun")


def Milestone1_Get_OpnenAQ_Dataset_Measurement_OpenAQStation_perStation(StationOpenAQ, parameter):
    
#Step 1 Choose the measurement country to import and parameter 
   
   res1 = 0
  
   for ii in range(1, MAX_RETRIES + 1):

    
      try:
       
         res1 = api.measurements(
             location=StationOpenAQ,
             parameter=parameter,
             date_to=dt_end,
             date_from=dt_begin,
             limit=10000,
             df=True)
 
    
      except openaq.exceptions.ApiError:
            time.sleep(5)
            if(ii == MAX_RETRIES):
                RetriesPassed_YesNo = 0
            continue
            
      else:
            break

  
   print(res1) 

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

#Step 3 Choose the measurement country to import and parameter
#
# Choose the station
#
# OpenAQStationCoordinates = ''


print("  STEP 2 ")

print("********")

print("Chosen OpenAQ Station: ")
     
OpenAQStation = 'US Diplomatic Post: Abu Dhabi' #Edit

print(OpenAQStation)


print("Completed Step 1 ")

print(">")

# Step 3 Choose parameter

print("  STEP 3 ")

print("********")


print("Parameter chosen")

parameter = 'pm25'

print(parameter)


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

res2 = Milestone1_Get_OpnenAQ_Dataset_Measurement_OpenAQStation_perStation(OpenAQStation, parameter)



if(RetriesPassed_YesNo == 1):

   print("Found these Stations in Coordinates")

   OpenAQStationunique = res2['location'].unique()

   print(OpenAQStationunique)


if(RetriesPassed_YesNo == 0):
  
  print("*****") 
  
  print("API Error")
    
  print("The API returned an error because it was unavailable after trying this many requests ")  
  
  print(MAX_RETRIES)
  
  print("Try to the process again after a few minutes")


# Step 6 Get Measurements CSV
#  
#  Choose unique selection 
#
#  Change   SelectionOpenAQChoose = " "


print("  STEP 6 ")

print("********")

print("Getting Measurements to CSV ")

SelectionOpenAQ = 0

SelectionOpenAQChoose = "Unique selection"

Milestone1_Get_Measurements_CSV_OpenAQStation(res2, SelectionOpenAQChoose, parameter, SelectionOpenAQ, dt_begin, dt_end)
