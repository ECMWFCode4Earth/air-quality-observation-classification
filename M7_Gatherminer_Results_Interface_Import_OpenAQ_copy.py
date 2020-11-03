# -*- coding: utf-8 -*-
"""
Created on Mon Oct 19 13:41:31 2020

@author: wegia
"""

import jsonlines
import ndjson
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import pecos



def Get_OpenAQ_attr_for_Gatherminder(df, Location_Subset, Parameter_Subset):
    #Requires OpenAQ attributes Country City Location Parameter sourceType 
    
    print(df)

    Dataset10 = []
        
    for Location in Location_Subset['location']: 
    
        
        #Location_Parameter = df[Location_Subset['location'] == Location]
        
        #print(Location_Parameter)
        
        print(Location)
        
        
        for Parameter in Parameter_Subset['parameter']:
                    
            Dataset_attr = []
    
            Country = df[Location == df.location].country
    
            City = df[Location == df.location].city
    
            Country = Country.drop_duplicates(keep='first')
 
            Country = Country.iloc[0]

            City = City.drop_duplicates(keep='first')

            City = City.iloc[0]  
   
            Dataset_attr.append(Country)
            Dataset_attr.append(City)
            Dataset_attr.append(Location)
            Dataset_attr.append(Parameter)
            
            Dataset10.append(Dataset_attr)
            #print(Dataset_attr)
                 
    Results = pd.DataFrame(Dataset10, columns=['COUNTRY','CITY','LOCATION','PARAMETER'])
    print(len(Results))   
    Results.to_csv(r'D:\AirNode\TechnicalStack\AirNode_Dependencies\Functionality\L_IoT\Gatherminer-master\example_data\openAQ_attr100_100.csv',index=False)                       

#    Results_openAQ = pd.DataFrame(df)
 #   print(len(Results_openAQ))   
  #  Results_openAQ.to_csv(r'D:\AirNode\TechnicalStack\AirNode_Dependencies\Functionality\L_IoT\Gatherminer-master\example_data\openAQ_dataset100.csv',index=False)                       


    return Results  

def Get_OpenAQ_Dataset_attr_for_Gatherminder(df, Location_Subset, Parameter_Subset):

    #Requires OpenAQ attributes Country City Location Parameter sourceType 
    
    print(df)

    Dataset10 = []
        
    for Location in Location_Subset['location']: 
    
        
        #Location_Parameter = df[Location_Subset['location'] == Location]
        
        #print(Location_Parameter)
        
        print(Location)
        
        
        for Parameter in Parameter_Subset['parameter']:
                    
            Dataset_attr = []
    
            Country = df[Location == df.location].country
    
            City = df[Location == df.location].city
    
            Country = Country.drop_duplicates(keep='first')
 
            Country = Country.iloc[0]

            City = City.drop_duplicates(keep='first')

            City = City.iloc[0]  
   
            Dataset_attr.append(Country)
            Dataset_attr.append(City)
            Dataset_attr.append(Location)
            Dataset_attr.append(Parameter)
            
            Dataset10.append(Dataset_attr)
            #print(Dataset_attr)
           
          #  print(Parameter.dtypes)
            
          #  print(df[['parameter']==Parameter])
            
            for df4 in df: 
         
                print(df4)
                
                print(Location)
                
                
                
                df5 = df4[df4['location']==Location['location']]
                
                df6 = df5[df5['parameter']==Parameter['parameter']]
                
                ResultsCSV_Dataset.append(df6['value'])
            
                
            
  #          ResultsCSV_Dataset = pd.DataFrame()
            
   # Results = pd.DataFrame(Dataset10, columns=['COUNTRY','CITY','LOCATION','PARAMETER'])
   # print(len(Results))   
   # Results.to_csv(r'D:\AirNode\TechnicalStack\AirNode_Dependencies\Functionality\L_IoT\Gatherminer-master\example_data\openAQ_attr100_100.csv',index=False)                       

#    Results_openAQ = pd.DataFrame(df)
#    print(len(Results_openAQ))   
 #   Results_openAQ.to_csv(r'D:\AirNode\TechnicalStack\AirNode_Dependencies\Functionality\L_IoT\Gatherminer-master\example_data\openAQ_dataset100.csv',index=False)                       


    return ResultsCSV_Dataset  

  #  Results_openAQ = pd.DataFrame(df)
   # print(len(Results_openAQ))   
  #  Results_openAQ.to_csv(r'D:\AirNode\TechnicalStack\AirNode_Dependencies\Functionality\L_IoT\Gatherminer-master\example_data\openAQ_dataset100.csv',index=False)                       


data_file1 = 'openAQ_PM25_3_copy.xlsx';

#df4 = pd.read_csv (r'openAQ_PM25_3_copy_2.csv',index_col=0)


df = pd.read_excel(data_file1, index_col=0)

#print(df4.dtypes)

print(df.dtypes)

Dataset2 = df[['utc','value','parameter','value_copy','value_copy1','value_copy2']].copy()

Dataset = df


Location_Subset = Dataset[['location']].copy()

Parameter_Subset = Dataset[['parameter']].copy()
 

print(len(Location_Subset))

Location_Subset.sort_values('location', ascending=False)
Location_Subset = Location_Subset.drop_duplicates(subset='location', keep='first')

Parameter_Subset.sort_values('parameter', ascending=False)
Parameter_Subset = Parameter_Subset.drop_duplicates(subset='parameter', keep='first')


Get_OpenAQ_attr_for_Gatherminder(df, Location_Subset, Parameter_Subset)

# Get_OpenAQ_Dataset_attr_for_Gatherminder(df, Location_Subset, Parameter_Subset)              
                    