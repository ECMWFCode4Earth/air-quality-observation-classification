# -*- coding: utf-8 -*-
"""
Created on Tue Dec  8 12:13:31 2020

@author: wegia
"""



import openaq

import pandas as pd

from pandas import json_normalize

from datetime import datetime, date, time, timezone

import requests

import time

import numpy as np

import csv


# Step 1 Initiatlise pyOpenAQ API
#
#  1 There are no edits 

print("  STEP 1 ")

print("********")

print("Initialise pyOpenAQ API")

api = openaq.OpenAQ()

MAX_RETRIES = 10

print("OpenAQ pyOpenAPI begun")



def Milestone1_notGet_OpenAQ_Dataset_Measurement_perStation(StationOpenAQCoordinates, Radius, parameter, dt_begin, dt_end):
    
#Step 1 Choose the measurement coordinate centre radius to import and parameter 
    
   res1 = api.measurements(coordinates=StationOpenAQCoordinates, parameter='pm25', radius=Radius, date_to=dt_end, date_from=dt_begin, df=True, limit=10000)
  
   
   print("Completed measurements ")

   return res1


def Milestone1_Get_Import_OpenAQ_Countries_OpenAQStations(OpenAQSelect):

   print(OpenAQSelect)  
     
   resp_attribute = api.locations(country=OpenAQSelect, df=True)
 
   print(resp_attribute['location'])
    
   return resp_attribute

def Milestone1_Get_Import_OpenAQ_Countries(OpenAQSelect):

 #  status, resp = api.cities()

   #print(resp)

   if(len(OpenAQSelect) == 0):

     resp_attribute = api.countries(df=True)

   else:
     
     print(OpenAQSelect)  
     
     resp_attribute = api.countries(country=OpenAQSelect, df=True)
  

   df2 = resp_attribute.code

   df3 = pd.DataFrame(df2)

   print(resp_attribute)


   return resp_attribute

def Milestone1_Get_OpenAQ_Dataset_Measurement_perStation(StationOpenAQCoordinates, Radius, parameter, dt_begin, dt_end):
    
#Step 1 Choose the measurement coordinate centre radius to import and parameter 
  

   res1 = []
   OpenAQStation = []
   
   for ii in range(1, MAX_RETRIES + 1):

      try: 
    
         if(len(parameter) == 1):
       
           OpenAQStation = api.measurements(
               coordinates=StationOpenAQCoordinates, 
               radius=Radius,
               parameter=parameter[0], 
               date_to=dt_end, 
               date_from=dt_begin, 
               index="utc",
               df=True, 
               limit=10000
               )
           
      #     res1 = []
             
           res1.append(OpenAQStation)
             
         else:  
     
            res1 = Milestone1_Get_OpenAQ_Dataset_Measurementexception_perStation(StationOpenAQCoordinates, Radius, parameter, dt_begin, dt_end)    
         
          #  res1 = api.measurements(coordinates=StationOpenAQCoordinates, radius=Radius, date_to=dt_end, date_from=dt_begin, df=True, limit=10000)
            
   
          #  res1 = api.measurements(
          #     coordinates=StationOpenAQCoordinates,
          #     radius=Radius, 
          #     date_to=dt_end, 
          #     date_from=dt_begin, 
          #     df=True, 
          #     limit=10000
          #     )
           # print(res1)
            
          #  res1.append(res)
            
      except openaq.exceptions.ApiError:
            time.sleep(5)
            continue
      else:
            break
    
  # OpenAQStation.append(res1)
   res1.append([])
   print("Completed measurements ")

   return res1
  
def Milestone1_OpenAQ_API_Get_Measurement(OpenAQSelects, OpenAQversion):
    
   
          
    Reqparameter = []
     
   
    Reqparameter.append(Milestone1_Getparameter(str(dt_begin.month)))
     
    Reqparameter.append(Milestone1_Getparameter(str(dt_begin.day)))
     
    Reqparameter.append(Milestone1_Getparameter(str(dt_end.month)))
     
    Reqparameter.append(Milestone1_Getparameter(str(dt_end.day)))
     
   
   
    parameterrequest1 = "https://u50g7n0cbj.execute-api.us-east-1.amazonaws.com/v1/measurements?" 
   
    paramerterrequestv2 = "https://u50g7n0cbj.execute-api.us-east-1.amazonaws.com/v2/measurements?"
                
    if(OpenAQversion == 0): 
        
        parameterrequest = parameterrequest1 + "date_from=" + str(dt_begin.year) + Reqparameter[0] +  Reqparameter[1]  + "T00%3A00%3A00%2B00%3A00&date_to=" + str(dt_end.year)  + Reqparameter[2]  + Reqparameter[3] + "T00%3A00%3A00%2B00%3A00&limit=10000&sort=desc&" + "coordinates=" + str(OpenAQSelects['coordinates']) + "&radius=" + str(OpenAQSelects['radius'])  + "&order_by=datetime"
        
    if(OpenAQversion == 1):
     
        parameterrequest = paramerterrequestv2 + "date_from="  + str(dt_begin.year) + Reqparameter[0] +  Reqparameter[1]  + "T00%3A00%3A00%2B00%3A00&date_to=" + str(dt_end.year)  + Reqparameter[2]  + Reqparameter[3] + "T00%3A00%3A00%2B00%3A00&limit=10000&offset=0&sort=desc&" + "coordinates="  + str(OpenAQSelects['coordinates']) + "&radius="  + str(OpenAQSelects['radius']) + "&order_by=datetime"
 
        if(OpenAQisMobile != 0):
        
           
           print(parameterrequest)
     
           if(OpenAQisMobile == "TRUE" or OpenAQisMobile == "FALSE"):
           
              parameterrequest += "&isMobile=" + OpenAQisMobile      
    
        if(OpenAQisAnalysis != 0):
           
           if(OpenAQisAnalysis == "TRUE" or OpenAQisAnalysis == "FALSE"):
           
              parameterrequest += "&isAnalysis=" + OpenAQisAnalysis
    
        if(OpenAQentity != 0):
          
           if(OpenAQsensorType == "goverment" or OpenAQsensorType == "research" or OpenAQsensorType == "community"):   

              parameterrequest += "&entity=" + OpenAQentity
    
        if(OpenAQsensorType != 0):

           if(OpenAQsensorType == "reference grade" or OpenAQsensorType == "low-cost sensor" ):   

              parameterrequest += "&sensorType=" + OpenAQsensorType

    if(len(OpenAQSelects['parameter']) > 0):
         
       parameterrequest += "&parameter=" + OpenAQSelects['parameter'][0] 
     

    print(parameterrequest)
    
    parameterrequest += "&page="
  
    return parameterrequest

def Milestone1_OpenAQ_API_Get_Measurements_APIoneStation(OpenAQSelects, OpenAQversion):

    
       
   OpenAQdf = []
  
   try:
       
    
     parametersort = "https://u50g7n0cbj.execute-api.us-east-1.amazonaws.com/v1/measurements?date_from=" + str(dt_begin) + "&date_to=" + str(dt_end) + "&limit=100&page=1&offset=0&country=AE&sort=desc&radius=1&order_by=datetime"  
    
#    "2000-01-01T00%3A00%3A00%2B00%3A00"
    
#    2021-02-05T12%3A00%3A00%2B00%3A00"

 #   response = requests.get("https://docs.openaq.org/v2/measurements?limit=100&page=1&offset=0&sort=desc&radius=1000")  
  
    

     
     print(OpenAQSelects['parameter'])

     
     parameterrequest = Milestone1_OpenAQ_API_Get_Measurement(OpenAQSelects, OpenAQversion)
   
     response = requests.get(parameterrequest + "1")
   
         
       #  "https://u50g7n0cbj.execute-api.us-east-1.amazonaws.com/v2/measurements?date_from=2020-03-01T00%3A00%3A00%2B00%3A00&date_to=2020-03-04T00%3A00%3A00%2B00%3A00&limit=10000&page=1&offset=0&sort=desc&coordinates=24.4244%2C54.4337&radius=100000&order_by=datetime")
         
   
     responseno = response.json()["meta"]
     
     print("Found results ")
     
     print(responseno["found"])
     
     responseno = int(responseno["found"]/OpenAQSelects["limit"])
     
     print(responseno)  
   
    
     
     if(response.status_code == 200):
            resp = response.json()["results"]
    
            OpenAQdfresp = pd.DataFrame(resp)
            OpenAQdfresp = Milestone2_Convert_Latlng(OpenAQdfresp)
           
          #  print(OpenAQdfresp["date"])  
            OpenAQdfresp = Milestone2_Convert_DateFormat(OpenAQdfresp)

            OpenAQdfresp.index = OpenAQdfresp['date.utc']
       
     
     OpenAQdf.append(OpenAQdfresp)
             
     OpenAQreq = range(2, responseno)
   
     
     for page_num in range(2, responseno + 1):

        print(" Request append results ") 
        print(str(page_num)) 
                
        OpenAQrequestparameterrequest = parameterrequest + "&page=" + str(page_num)           

        response = requests.get(OpenAQrequestparameterrequest)
     
     #  print(response.json())
      
        if(response.status_code == 200):
            resp = response.json()["results"]
    
            OpenAQdfresp = pd.DataFrame(resp)
          #  print(OpenAQdfresp["date"])  
           
            OpenAQdfresp = Milestone2_Convert_Latlng(OpenAQdfresp)
            OpenAQdfresp = Milestone2_Convert_DateFormat(OpenAQdfresp)
           
            OpenAQdfresp.index = OpenAQdfresp['date.utc']
       
            responseno = resp.json()["meta"]
     
            print("Found results next request ")
     
            
            print(responseno["found"])
     
            responseno = int(responseno["found"]/OpenAQSelects["limit"])
     
            print(responseno)  
   
     
        OpenAQdf.append(OpenAQdfresp)
        
     
   except:
   
      pass
  
   print(response.status_code)
   
 #  print(OpenAQdf)
   
   return OpenAQdf



def Milestone1_Get_Parameters(OpenAQSelect, Radius, parameterselected, dt_begin, dt_end):
   
   OpenAQSelects = {
      "radius": Radius,
      "coordinates": OpenAQSelect,
    #  "location": station1,
      "parameter": parameterselected,
      "date_from": dt_begin,
      "date_to": dt_end,
      "limit": 10000
   }

   print(OpenAQSelects['radius'])

   return OpenAQSelects


def Milestone1_Getparameter(Reqparameter):
    
    if(int(Reqparameter) < 10):
       
        Requestparameter = "-0" + Reqparameter

    else:

        Requestparameter = "-" + Reqparameter 
        
    return Requestparameter
    


def Milestone1_Get_Import_Count_OpenAQ_Stations(OpenAQselection):
   
   print(OpenAQselection)
   
   
   if(len(OpenAQselection) > 0):
 


      OpenAQStations = []

      OpenAQStation = []

      OpenAQuniqueStations = []

      

      for OpenAQ_Station in OpenAQselection:
    
       
         print(OpenAQ_Station)
       
         OpenAQStationunique = OpenAQ_Station['country'].unique()
         
         print(OpenAQStationunique)   
         
         OpenAQStationsunique = OpenAQ_Station['city'].unique()

         for OpenAQStationsunique1 in OpenAQStationsunique:

            OpenAQStations.append(OpenAQStationsunique1)
         
         
         OpenAQStationsselect = OpenAQ_Station['location'].unique()

         
         OpenAQStationsselects = OpenAQ_Station['locationId'].unique()

         print(len(OpenAQStationsselect))
  
         print(len(OpenAQStationsselects))

         for OpenAQStationsunique in OpenAQStationsselect:

            OpenAQuniqueStations.append(OpenAQStationsunique)
  
            OpenAQStationappend = []
            
            print(OpenAQStationsunique)
            
            OpenAQparameter = OpenAQ_Station[OpenAQ_Station['location']==OpenAQStationsunique]
              
        #    print(OpenAQparameter)
            
            OpenAQStationappend.append(OpenAQparameter['locationId'][0])
             
            print(OpenAQStationappend)
            
            OpenAQStationappend.append(OpenAQStationsunique)
            
            OpenAQparameters = len(OpenAQparameter[OpenAQparameter['parameter']=='bc'])
            
            OpenAQStationappend.append(OpenAQparameters)
  
            OpenAQparameters = len(OpenAQparameter[OpenAQparameter['parameter']=='co'])
            
            OpenAQStationappend.append(OpenAQparameters)
   
            OpenAQparameters = len(OpenAQparameter[OpenAQparameter['parameter']=='no2'])
            
            OpenAQStationappend.append(OpenAQparameters)
  
            OpenAQparameters = len(OpenAQparameter[OpenAQparameter['parameter']=='o3'])
            
            OpenAQStationappend.append(OpenAQparameters)
  
            OpenAQparameters = len(OpenAQparameter[OpenAQparameter['parameter']=='pm10'])
            
            OpenAQStationappend.append(OpenAQparameters)

            OpenAQparameters = len(OpenAQparameter[OpenAQparameter['parameter']=='pm25'])
           
            OpenAQStationappend.append(OpenAQparameters)
 
    
            OpenAQStationappend.append(len(OpenAQ_Station.index))
 
  
            print(OpenAQ_Station) 

            OpenAQStation.append(OpenAQStationappend)

            print(OpenAQStationappend)
            
            
            
#            OpenAQparameters = OpenAQparameter[OpenAQparameter['parameter']=='o3']
            
 #           OpenAQStationappend(OpenAQparameters)

 #           'pm10','pm25', # 'so2'
                     
         #   OpenAQStation.append(OpenAQStationappend) 
 
      OpenAQunique = pd.DataFrame(OpenAQStation, columns=['locationid','location','bc','co','no2','o3','pm10','pm25', 'Total'])
            
      print(OpenAQunique)
      
      print("Found these Stations in selection")

      OpenAQStations = pd.DataFrame(OpenAQStations, columns=["city"])

      
      OpenAQStationdfunique = pd.DataFrame(OpenAQuniqueStations, columns=["locations"])

      print(OpenAQStations['city'].unique())
      
      print(OpenAQStationdfunique['locations'].unique())

      
      
def Milestone2_Convert_Latlng(DatasetOpenAQ):
    
#How to split column into two columns
#https://www.geeksforgeeks.org/split-a-text-column-into-two-columns-in-pandas-dataframe/
 
#   print(DatasetOpenAQ.dtypes) 
 
  # {  'latitude': 40.437622, 'longitude': -79.979849}

   DatasetOpenAQ[['lat','lng']] = DatasetOpenAQ.coordinates.apply(lambda x: pd.Series(str(x).split(",")))
  
   Dataset_split = DatasetOpenAQ.lat.apply(lambda x: pd.Series(str(x).split("'latitude':")))

   DatasetOpenAQ.insert(loc=len(DatasetOpenAQ.columns), column="coordinate.latitude",value=Dataset_split[1])

   DatasetOpenAQ[['lngselect','lngapply']] = DatasetOpenAQ.lng.apply(lambda x: pd.Series(str(x).split("':")))

 #  print()

   SelectStationlng = DatasetOpenAQ.lngapply.apply(lambda x: pd.Series(str(x).split("}")))

   DatasetOpenAQ.insert(loc=len(DatasetOpenAQ.columns), column="coordinate.longitude",value=SelectStationlng[0])

   DatasetOpenAQ.drop(['lat','lng','coordinates','lngselect','lngapply'], axis=1, inplace=True)

   print(DatasetOpenAQ.dtypes) 

   return DatasetOpenAQ
      
def Milestone2_Convert_DateFormat(DatasetOpenAQ):
    
#How to split column into two columns
#https://www.geeksforgeeks.org/split-a-text-column-into-two-columns-in-pandas-dataframe/
 
  # print(DatasetOpenAQ.dtypes) 

   DatasetOpenAQ[['Dateutc','Datelocal']] = DatasetOpenAQ.date.apply(lambda x: pd.Series(str(x).split(",")))


   Dataset_split = DatasetOpenAQ.Dateutc.apply(lambda x: pd.Series(str(x).split("':")))
  
   DatasetOpenAQ['date.utc'] = pd.to_datetime(Dataset_split[1])

   pd.to_datetime(DatasetOpenAQ['date.utc'])

   DatasetOpenAQ.drop(columns=['Dateutc','Datelocal','date'], inplace=True)

   print(DatasetOpenAQ.dtypes) 
   
   return DatasetOpenAQ


def Milestone1_Get_OpenAQ_Dataset_Measurementexception_perStation(StationOpenAQCoordinates, Radius, parameter, dt_begin, dt_end):
    
   OpenAQStations = []
   iteration = 0
   
   status = 0
   
   parameter_selection = ['pm25','bc','co','o3','pm10','pm25','so2']
 
   #for parameters in parameter_selection:
       
   try:
       # print(parameters)
         
         
       OpenAQselection = "coordinates='" + StationOpenAQCoordinates + "', radius='" + str(Radius) + "', parameter='" 
       
       #+ "', date_to=" + str(dt_end) + " , date_from=" + str(dt_begin) + " , df=True" +  " , index=" + "utc" + " , limit= 10000" 
         
       print(OpenAQselection)
         
       res1 = api.measurements(coordinates=StationOpenAQCoordinates, radius=Radius,date_to=dt_end, date_from=dt_begin, df=True, limit=10000)
            
       #  print(res1)
         
         
         
          #  res1 = api.measurements(
          #     coordinates=StationOpenAQCoordinates,
          #     radius=Radius, 
          #     date_to=dt_end, 
          #     date_from=dt_begin, 
          #     df=True, 
          #     limit=10000
          #     )
      
       OpenAQStations.append(res1)  
      
   except openaq.exceptions.ApiError:
       time.sleep(5)
       pass
   else:
       print(" Exception ")
       pass
    
       
    #  print(status)
         
   
   iteration = iteration + 1
   
   
   return OpenAQStations  
          
          

def Milestone1_Get_Measurements_CSV_OpenAQStation(OpenAQ_Stations, SelectionOpenAQChoose, parameter, SelectionOpenAQ, dt_begin, dt_end, SelectionDatasetOpenAQ):
    
   OpenAQDataset = r'OpenAQ_Dataset'
 
   SelectedOpenAQ = "Selection"
   
   if(SelectionOpenAQ == 0):
     SelectedOpenAQ = "One Station"
      
   if(SelectionOpenAQ == 1):
     SelectedOpenAQ = "CoordinateCentreandRadius"
  
   if(SelectionOpenAQ == 2):
     SelectedOpenAQ = "Country"
   
   
   
   OpenAQDatasetcomplete = OpenAQDataset + " " + SelectionOpenAQChoose + " " + " " + SelectedOpenAQ + " " +  str(dt_begin) + " to " + str(dt_end) + ".csv" 
    
   print("Printed OpenAQ import to ")
   
   print( OpenAQDatasetcomplete)
   
    
   if(SelectionDatasetOpenAQ == 0):   
    OpenAQ_Stations.to_csv(OpenAQDatasetcomplete, mode='w', index=False)                       
 
   if(SelectionDatasetOpenAQ == 1):
    OpenAQ_Stations.to_csv(OpenAQDatasetcomplete, header=False, index=False, mode='a+') 


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
    
 
     
OpenAQStationCoordinates = "51.0406%2C3.7349" # "24.4244%2C54.4337" # "34.60638%2C58.43194" # "35.94599%2C96.96093" # "24.4244%2C54.4337"


OpenAQLatselect = ["51.04068942%2C3.73497147968531"]


# "35.945993%2C96.960939" # 

# "-34.60638%2C-58.43194" #Edit Lat, Lng

Radius = 10500 # Edit in metres must be more than 1  i.e. min 5

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

print("Parameter chosen")

if(SelectEveryParameter_YesorNo == 0):
    
   parameter_selection = []

   parameter_selection.append(parameter)

   print(parameter_selection)

if(SelectEveryParameter_YesorNo == 1):
    
   print("Every parameter at selected or chosen OpenAQ station") 

   parameter_selection = [] # ['bc','co','no2','o3','pm10','pm25','so2']

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

dt_end = date(2020,3,4) # Edit

print("  STEP 4 ")

print("********")


print("Getting OpenAQ dataset applying pyOpenAQ API from ") 
print(dt_begin)
print(" to ")
print(dt_end)
print(" for one OpenAQ Station and one parameter ")


# Changes these to select these

OpenAQisMobile = 0 # Edit TRUE or FALSE
                       
OpenAQisAnalysis = 0 # Edit TRUE or FALSE
                             
OpenAQentity = 0 # Edit  government, research, community                            

OpenAQsensorType = 0 # Edit 'reference grade' or 'low-cost sensor'

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

#res2 = Milestone1_notGet_OpnenAQ_Dataset_Measurement_perStation(OpenAQStationCoordinates, Radius, parameter_selection, dt_begin, dt_end)

# res2 = Milestone1_Get_OpenAQ_Dataset_Measurement_perStation(OpenAQStationCoordinates, Radius, parameter_selection, dt_begin, dt_end)


iterationamount = 0

OpenAQSelects = Milestone1_Get_Parameters(OpenAQStationCoordinates, Radius, parameter_selection, dt_begin, dt_end)

print(OpenAQSelects)

OpenAQversion = 1 # Edit 0 Version 1 and 1 Version  2 OpenAQ API request

res2 = Milestone1_OpenAQ_API_Get_Measurements_APIoneStation(OpenAQSelects, OpenAQversion)

# OpenAQselection = Milestone1_Get_Import_OpenAQ_Dataset_One_Statonselect(OpenAQSelects, iterationamount, OpenAQrequest)


Milestone1_Get_Import_Count_OpenAQ_Stations(res2)



if(len(res2[0]) == 0):
  
  print("*****") 
  
  print("API Error")
    
  print("The API returned an error because it was unavailable after trying this many requests ")  
  
  print(MAX_RETRIES)
  
  print("Try to the process again after a few minutes")

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

SelectionOpenAQChoose = "Unique  debugged radius " + str(Radius) # + OpenAQStationCoordinates



if(len(res2[0]) > 0):
    
    SelectionDatasetOpenAQ = 0
    
    Milestone1_Get_Measurements_CSV_OpenAQStation(res2[0], SelectionOpenAQChoose, parameter_selection, SelectionOpenAQ, dt_begin, dt_end, SelectionDatasetOpenAQ)


iterationamount = 1

SelectionDatasetOpenAQ = 1

for OpenAQ_Station in res2:

    
   if(len(res2) > iterationamount):
   
     Milestone1_Get_Measurements_CSV_OpenAQStation(res2[iterationamount], SelectionOpenAQChoose, parameter_selection, SelectionOpenAQ, dt_begin, dt_end, SelectionDatasetOpenAQ)

     iterationamount = iterationamount + 1 

print("Completed Step 6 ")

print(">")
