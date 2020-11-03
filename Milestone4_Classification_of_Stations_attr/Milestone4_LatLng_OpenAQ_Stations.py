# -*- coding: utf-8 -*-
"""
Created on Tue Nov  3 15:00:47 2020

@author: wegia
"""



import openaq

import pandas as pd

from pandas.io.json import json_normalize

api = openaq.OpenAQ()

status, resp = api.cities()

print(resp)

resp_attribute = api.countries(df=True)

df1 = pd.json_normalize(resp)

# print(respC.code)

# print(df1.ix[0])

res = api.locations(df=True)

# print(res)

df = pd.DataFrame(res)


df2 = resp_attribute.code

df3 = pd.DataFrame(df2)

print(resp_attribute.code)

print(res['coordinates.latitude'])
      
     # .coordinates.latitude)
      
     
      #, ",",res.coordinates.longitude,"|")

print(len(df3))

df_DF = [];


for index, respC in df3.iterrows():
    
#    print(respC.to_string())
    
 #   print(respC[0])
    
    df4 = respC.astype("|S")
    
 #   print(df4.dtypes)
    
    result1 = api.locations(country=respC[0], df=True)

 #   print(result1)
    
    df_3 = []

    for index, res1 in result1.iterrows():
   
  #     print(res1)   
       
        
       
       print(res1['coordinates.latitude'], ",",res1['coordinates.longitude'],"|")

      # df5 = [res1['coordinates.latitude'],",",res1['coordinates.longitude'],"|", res1['location']]
 
       df_1 = [res1['coordinates.latitude'],",",res1['coordinates.longitude'],"|"]

       
 #      df_2 = pd.DataFrame(df5)

       df_3.append(df_1) 
       
    df_DF.append(df_3)   
   
df_7_DF = pd.DataFrame(df_DF) 

#print(len(df_7_DF))

   
    #  print(df_2.astype("|S"))

#       df5 = pd.DataFrame(df5)
       
 #      df7 = df5.to_string()

  #     print(df7)


Results.to_csv(r'openAQ_100Latlngattr100.csv',index=False)       