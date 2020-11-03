# -*- coding: utf-8 -*-
"""
Created on Tue Nov  3 15:06:27 2020

@author: wegia
"""



import openaq

import pandas as pd

from pandas.io.json import json_normalize

import matplotlib.pyplot as plt

from datetime import datetime, date, time, timezone



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
             
            df_DF.append(res2['location'])
       
     
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



def Milestone3_Get_Import_OpenAQ_Dataset_One_Staton(OpenAQStation):

   print(OpenAQStation)  
    
   res_1 = api.measurements(location=OpenAQStation, parameter='pm25', date_to=dt_end, date_from=dt_begin, limit=10000, df=True)

   #print(res_1.dtypes)


 #  res_1['date.utc'] = pd.to_datetime(res1['date.utc']).dt.tz_localize(None)

   res_1 = res_1[res_1.value != -999.00]

   res_1.set_index('date.utc')

   print(res_1)
   print(res_1['value'])

   print(res_1['date.utc'])

   print(res_1['value'])


   return res_1


OpenAQ_Countries = Milestone3_Get_Import_OpenAQ_Countries()

OpenAQStation = Milestone3_Get_Import_OpenAQ_EveryStation(OpenAQ_Countries)

Milestone3_Get_Import_OpenAQ_Dataset_One_Staton(OpenAQStation)