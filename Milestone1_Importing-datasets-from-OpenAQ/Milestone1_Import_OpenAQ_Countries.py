# -*- coding: utf-8 -*-
"""
Created on Wed Nov  4 11:52:37 2020

@author: wegia
"""




import openaq

import pandas as pd


from pandas.io.json import json_normalize

import matplotlib.pyplot as plt

from datetime import datetime, date, time, timezone


# https://github.com/openaq/openaq-api/issues/392


def Milestone1_Get_Import_OpenAQ_Countries():


   print("Milestone1_Get_Import_OpenAQ_Countries")
  
   resp_attribute = api.countries(df=True)

   return resp_attribute

def Milestone1_Get_Import_OpenAQ_Countries_code(resp_attribute):

   print("Milestone1_Get_Import_OpenAQ_Countries_code")

   print(resp_attribute)
  
   df2 = resp_attribute.code

  # print(df2)

   df3 = pd.DataFrame(df2)

   #print(resp_attribute.code)

#   print(len(df3))

   print("Completed Milestone1_Get_Import_OpenAQ_Countries")

   return df3

def Milestone1_Get_Import_OpenAQ_Cities_percountry(OpenAQcountry):

   print("Milestone1_Get_Import_OpenAQ_Cities_percountry")
   
   print("Input")
   
   print(OpenAQcountry)
   
   resp = api.cities(df=True, limit=10000)

   # display the first 10 rows
  # print(resp.info())   
    
   
   
    #  print(country)      
       
      # res_location = api.locations(country=country.name, df=True)

 #     print(country.code)

   compare = "country=='" + OpenAQcountry + "'"

   res1_location = resp.query(compare)

   print("Completed Milestone1_Get_Import_OpenAQ_Cities_percountry(OpenAQcountry)")
   
   return res1_location


print("Getting OpenAQ dataset of countries attributes ") 

    
api = openaq.OpenAQ()

OpenAQCountries = Milestone1_Get_Import_OpenAQ_Countries()

print(OpenAQCountries.info())

OpenAQCountries_Codes = Milestone1_Get_Import_OpenAQ_Countries_code(OpenAQCountries)

print(OpenAQCountries_Codes.info())    

print(OpenAQCountries_Codes)  
