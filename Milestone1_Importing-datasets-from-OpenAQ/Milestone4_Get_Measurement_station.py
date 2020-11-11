# -*- coding: utf-8 -*-
"""
Created on Wed Nov 11 11:03:49 2020

@author: wegia
"""


import requests


def Get_Measurements_APIoneStation(station1):

   parameters1 = {
      "country": station1,
      "parameter": "pm25"
   }


   try:
    
     response = requests.get("https://api.openaq.org/v1/measurements", params=parameters1)

   except:
      pass
  
   print(response.status_code)

   print(response.json())

   return response.json()


Get_Measurements_APIoneStation('Skver')

