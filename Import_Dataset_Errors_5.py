# -*- coding: utf-8 -*-
"""
Created on Fri Jul  3 18:07:08 2020

@author: wegia
"""
import jsonlines
import ndjson
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import pecos


data = []

with jsonlines.open('OpenAQ_1.ndjson') as reader:
    for obj in reader:
        #print(obj)
        obj1 = pd.Series(obj)
        #pd.read_csv(obj)
        data.append(obj1)

Dataset = pd.DataFrame(data)


def plot_df(df, x, y, title="", xlabel='Date', ylabel='Value', dpi=100):
    plt.figure(figsize=(16,5), dpi=dpi)
    plt.plot(x, y, color='tab:red')
    plt.gca().set(title=title, xlabel=xlabel, ylabel=ylabel)
    plt.show()


def Get_OpenAQ_times_series_every_15mins_for_one_day(start_time, interval):
    
    
    result = (pd.DataFrame(columns=['NULL'],
                  index=pd.date_range('2017-12-31T00:00:00Z','2018-01-01T01:00:00Z', 
                                      freq=interval))
       .between_time('00:00','23:45')
       .index.strftime('%Y-%m-%dT%H:%M:%SZ')
       .tolist())
    result2 = pd.to_datetime(result).tz_localize(None)
    result1 = pd.Series(result2)
    print(result1)
    return result1 
    

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
#    Results.to_csv(r'D:\AirNode\TechnicalStack\AirNode_Dependencies\Functionality\L_IoT\Gatherminer-master\example_data\openAQ_attr.csv',index=False)                       
    return Results                
                    
 #   for Country in df.country:

  #      for City in df[Country == df.country].city:    
def Get_OpenAQ_nearestroad_to_location_from_GoogleMaps_RoadAPI(lat, lng):
    
    import googlemaps
    
#    pd.Series
    
    Location_info = (lat, lng)
    
    #Location_Attr = pd.DataFrame(Location_info)
    
#    Location_Attr.append(lng)
    
    print(Location_info)
    
    gmaps = googlemaps.Client(key='')
    
        
    Results = gmaps.nearest_roads(Location_info)
  
    Results2 = gmaps.snapped_speed_limits(Location_info)
        
  #  print(Results2)
    
    print(Results)
    
    return Results
    
def Get_OpenAQ_DateTime_index_from_Date_Attribute(Dataset):
    
    
    Dataset2 = Dataset.date.apply(lambda x: pd.Series(str(x).split(",")))

    Dataset_split = Dataset2[1].apply(lambda x: pd.Series(str(x).split("'local':")))


    print(Dataset_split[1])

    Dataset_split = Dataset_split[1].apply(lambda x: pd.Series(str(x).split("}")))

    print(Dataset_split)


  #  Dataset_results_notformated = str(Dataset_split[0])

  #  print(Dataset_results_notformated)

  #  Dataset_split[0] = str(Dataset_split[0])

    #print(Dataset_split[0][:-5])


    Dataset_results_notformated = [sub[:-7] for sub in Dataset_split[0]]

    Dataset_results_notformated = [sub[2:22] for sub in Dataset_results_notformated]

        

    print("Dataset_results")

    print(Dataset_results_notformated)

 #   Dataset_split[0] = pd.to_datetime(Dataset_split[0], utc=True)

    Dataset_result = pd.to_datetime(Dataset_results_notformated).tz_localize(None)

    print(Dataset_result)
    
    
  #  print(Dataset_result.dtypes)

#    print(Dataset_result)

    
    return Dataset_result
    

print(Dataset[['date','value','parameter','location']])

print(Dataset.coordinates.iloc[0])
lat1 = Dataset.coordinates.iloc[100]['latitude']
lng1 = Dataset.coordinates.iloc[100]['longitude']

print(lat1)
print(lng1)

# Results_nearestroad = Get_OpenAQ_nearestroad_to_location_from_GoogleMaps_RoadAPI(lat1, lng1)


print(Dataset.dtypes)

#How to split column into two columns
#https://www.geeksforgeeks.org/split-a-text-column-into-two-columns-in-pandas-dataframe/

Dataset[['Dateutc','Datelocal']] = Dataset.date.apply(lambda x: pd.Series(str(x).split(",")))

Dataset_split = Dataset.Dateutc.apply(lambda x: pd.Series(str(x).split("'utc':")))

print(Dataset_split[1])

Dataset['utc'] = pd.to_datetime(Dataset_split[1]).dt.tz_localize(None)

print(Dataset['utc'])

pd.to_datetime(Dataset['utc'])

print(Dataset.dtypes)


Dataset_index_DateTime = Get_OpenAQ_DateTime_index_from_Date_Attribute(Dataset)


Dataset['local'] = Dataset_index_DateTime


Dataset2 = Dataset[['utc','value','parameter','location','local']].copy()

pd.to_datetime(Dataset2['utc'])
#Dataset2.set_index('utc')

Location_Subset = Dataset[['location']].copy()

Parameter_Subset = Dataset[['parameter']].copy()
 

print(len(Location_Subset))

Location_Subset.sort_values('location', ascending=False)
Location_Subset = Location_Subset.drop_duplicates(subset='location', keep='first')

Parameter_Subset.sort_values('parameter', ascending=False)
Parameter_Subset = Parameter_Subset.drop_duplicates(subset='parameter', keep='first')


#Location_Subset.drop_duplicates('location')

print(Location_Subset)

print(len(Location_Subset))


print(Location_Subset.dtypes)


Dataset_local = Dataset2['local']
Dataset_utc = Dataset2['utc']
Dataset_utclocal = Dataset2[['utc','local']].copy()

Dataset_local.sort_values(ascending=False)
Dataset_local = Dataset_local.drop_duplicates(keep='first')

Dataset_utc.sort_values(ascending=False)
Dataset_utc = Dataset_utc.drop_duplicates(keep='first')

Dataset_utclocal.sort_values('local', ascending=False)
Dataset_utclocal = Dataset_utclocal.drop_duplicates(subset='local', keep='first')


Dataset2['year'] = Dataset2['utc'].dt.year
Dataset2['month'] = Dataset2['utc'].dt.month
Dataset2['day'] = Dataset2['utc'].dt.day

print(Dataset2.utc.max())


Dataset_year = Dataset2[Dataset2.year == Dataset2.iloc[22]['year']]
Dataset_year = Dataset_year[Dataset_year.month == Dataset2.iloc[22]['month']]
Dataset_year = Dataset_year[Dataset_year.day == Dataset2.iloc[22]['day']]

#https://www.w3resource.com/python-exercises/pandas/datetime/pandas-datetime-exercise-3.php

print(Dataset_year.utc.min())

#print(Dataset2[Dataset2.year =='2017'].utc.min())

#print(Dataset2[Dataset2.year =='2017'].local.min())


print(Dataset2.local.max())

Dataset2.index = Dataset2['utc']
#Dataset2.sort_index()

#import datetime

# extracting date from timestamp
#Dataset2['Date2'] = [datetime.datetime.date(d) for d in Dataset2['utc']] 

# extracting time from timestamp
#Dataset2['Time'] = [datetime.datetime.time(d) for d in Dataset2['utc']] 


#Dataset2.sort_values('Time', ascending=False)
#Dataset2 = Dataset2.drop_duplicates(subset='Time', keep='first')


#print(Dataset_utclocal)

#print(Dataset2[['Time','Date2','utc']])

#print(Dataset2.dtypes)


Timesteps_utc = Get_OpenAQ_times_series_every_15mins_for_one_day(0,'15T')

Timesteps_utc_length = len(Timesteps_utc)

Dataset_Attributes = Get_OpenAQ_attr_for_Gatherminder(Dataset, Location_Subset, Parameter_Subset)

Test_Attr_Length = len(Dataset_Attributes)

#pd.to_datetime(Dataset2.index)

#LocationId = Dataset2.groupby('location').groups


#plot_df(df, x=Dataset2.index, y=Dataset2.value, title='Monthly anti-diabetic drug sales in Australia from 1992 to 2008.')    

Test_results_location_subset = []


Test_results_output = []


i = 0

pm2 = []

for LocationId in Location_Subset['location']:
 
    print(LocationId)
  
    Test_results_location_subset_parameter = []
    
    Test_results_location_subset_parameter.append(LocationId)
    
    Dataset3 = Dataset2[Dataset2['location']==LocationId]
    
    
    pd.to_datetime(Dataset3['local'])
    Test_results_location_subset_parameter_subset = Dataset3[['parameter']].copy() 
         
    #print(Test_results_location_subset_parameter_subset)
    
    Test_results_location_subset_parameter_subset.sort_values('parameter', ascending=False)
    Test_results_location_subset_parameter_subset = Test_results_location_subset_parameter_subset.drop_duplicates(subset='parameter', keep='first')

    for parameter in Parameter_Subset['parameter']:
    
    #Test_results_location_subset_parameter_subset['parameter']:
           
        print(parameter)
        
        Test_results_parameter = []
        
        Test_results_parameter.append(parameter)
        
        Dataset4 = Dataset3[Dataset3['parameter']==parameter]      

        Dataset4['min'] = Dataset4['utc'].dt.minute

        Dataset4['hour'] = Dataset4['utc'].dt.hour

        Dataset4['year'] = Dataset4['utc'].dt.year
        
        Dataset4['month'] = Dataset4['utc'].dt.month

        Dataset4['day'] = Dataset4['utc'].dt.day
        
        Dataset4.index = Dataset4['utc']
        
        pd.to_datetime(Dataset4['utc'])

        print(Dataset4)

        Dataset4.sort_index()  

        Dataset5 = Dataset4;

        # Initialize logger
        pecos.logger.initialize()

        # Create a Pecos PerformanceMonitoring data object
        pm1 = pecos.monitoring.PerformanceMonitoring()


        pm1.add_dataframe(Dataset4)

        clocktime = pecos.utils.datetime_to_clocktime(pm1.df.index)
 
        #print(clocktime) 
 
       # time_filter = pd.Series((clocktime >= 0*3600) & (clocktime < 24*3600), index=pm1.df.index) 

       # print("Time filter")

       # print(time_filter) 
   
        Test_results_output.append(Timesteps_utc.isin(Dataset4.utc))
                
        
       # for Time_step in Timesteps_utc:
    
          #  print(Time_step)
            
            
          #  print(Dataset4.utc.isin(np.array(Time_step).astype('datetime64[ns]')))
          #  print(Dataset4.utc.isin(Time_step1).any)
          #  print(Time_step)
          #  print(Dataset4.utc)
            #print()
            
          #  if(Dataset4.utc.isin(np.array(Time_step).astype('datetime64[ns]')).any):
          #      Test_results_output_timesteps.append(1)
          #  else:
          #      Test_results_output_timesteps.append(0)
                
       # pm1.add_time_filter(time_filter)       
        
        
        pm1.check_missing()
        
       # pm1.check_timestamp(86400)
        
# Check for corrupt data values
        pm1.check_corrupt([-999.000000],'value') 

# Add a composite signal which compares measurements to a model
#wave_model = np.array(np.sin(10*clock_time/86400))
#wave_measurments = pm.df[pm.trans['Wave']]
#wave_error = np.abs(wave_measurments.subtract(wave_model,axis=0))
#wave_error.columns=['Wave Error C', 'Wave Error D']
#pm.add_dataframe(wave_error)
#pm.add_translation_dictionary({'Wave Error': ['Wave Error C', 'Wave Error D']})

# Check data for expected ranges

        pm1.check_range([0, 10000000], 'value')



        pm1.check_range([2017, 2018], 'year')
        pm1.check_corrupt([2,3,4,5,6,7,8,9,10,11],'month')
        pm1.check_corrupt([2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30],'day')
        
        

        #print(pm1.test_results)
        
        Test_results_parameter.append(len(pm1.test_results))
       # pecos.graphics.plot_test_results(Dataset5,pm1.test_results)
           
        Test_results_parameter.append(pm1.test_results)
        Test_results_parameter.append(Dataset5)
        
        Test_results_location_subset_parameter.append(Test_results_parameter)
        
        print(pm1.test_results)
        print(Dataset5)
        
        #i = i + 1
       

    Test_results_location_subset.append(Test_results_location_subset_parameter)
 
    

Test_results_output_length = len(Test_results_output)    


Results_openAQ = pd.DataFrame(Test_results_output)
print(len(Results_openAQ))   
Results_openAQ.to_csv(r'D:\AirNode\TechnicalStack\AirNode_Dependencies\Functionality\L_IoT\Gatherminer-master\example_data\openAQ_dataset100.csv',index=False)                       
    

# Initialize logger
pecos.logger.initialize()

# Create a Pecos PerformanceMonitoring data object
pm = pecos.monitoring.PerformanceMonitoring()

# Populate the object with a DataFrame and translation dictionary
#data_file = 'simple.xlsx'
#df = pd.read_excel(data_file, index_col=0)
pm.add_dataframe(Dataset2)
#pm.add_translation_dictionary({'Wave': ['C','D']}) # group C and D

# Check the expected frequency of the timestamp
#pm.check_timestamp(900)
#pd.set_option('display.max_rows', None)

#print(Dataset['value'])

# Generate a time filter to exclude data points early and late in the day
#clock_time = pecos.utils.datetime_to_clocktime(pm.df.index)
#time_filter = pd.Series((clock_time > 3*3600) & (clock_time < 21*3600), 
#                        index=pm.df.index)
#pm.add_time_filter(time_filter)

# Check for missing data
pm.check_missing()
        
# Check for corrupt data values
pm.check_corrupt([-999.000000],'value') 

# Add a composite signal which compares measurements to a model
#wave_model = np.array(np.sin(10*clock_time/86400))
#wave_measurments = pm.df[pm.trans['Wave']]
#wave_error = np.abs(wave_measurments.subtract(wave_model,axis=0))
#wave_error.columns=['Wave Error C', 'Wave Error D']
#pm.add_dataframe(wave_error)
#pm.add_translation_dictionary({'Wave Error': ['Wave Error C', 'Wave Error D']})

# Check data for expected ranges
pm.check_range([0, 10000000], 'value')

pm.check_range([0, 10000000], 'value')
#pm.check_range([-1, 1], 'Wave')
#pm.check_range([None, 0.25], 'Wave Error')


print(pm.test_results)

# Check for stagnant data within a 1 hour moving window
#pm.check_delta([0.0001, None], 'value', 3600) 
#pm.check_delta([0.0001, None], 'B', 3600) 
#pm.check_delta([0.0001, None], 'Wave', 3600) 
    
# Check for abrupt changes between consecutive time steps
#pm.check_increment([None, 0.6], 'value') 

# Compute the quality control index for A, B, C, and D
mask = pm.mask[['value']]
QCI = pecos.metrics.qci(mask, pm.tfilter)

# Generate graphics
test_results_graphics = pecos.graphics.plot_test_results(pm.df, pm.test_results)
Dataset.plot(ylim=[1,1.5], figsize=(7.0,3.5))
plt.savefig('custom.png', format='png', dpi=500)

# Write test results and report files
pecos.io.write_test_results(pm.test_results)
pecos.io.write_monitoring_report(pm.df, pm.test_results, test_results_graphics, 
                                 ['custom.png'], QCI)

for Test_results_location in Test_results_location_subset:
    
    for Test_Parameter in Test_results_location[1:]:
      
        if(Test_Parameter[1] > 0):
            
           Dataset_results = Dataset[Dataset['location']==Test_results_location[0]] 

           print(Dataset_results[['local','value','parameter','location']])
                 
           Dataset_results2 = Dataset_results[Dataset['parameter']==Test_Parameter[0]] 
             
           print(Dataset_results2[['local','value','parameter','location']])
           #print(Test_results_location[0])
          # print(Test_Parameter[0])
          # print(Test_Parameter[2])  
           pd.to_datetime(Dataset_results2['local'])
           #print(Dataset_results2['utc'].dt.year) 
           #print(Dataset_results2['utc'].dt.month)
           #print(Dataset_results2['utc'].dt.day)
           #print(Dataset_results2)
           
           Dataset_results2.index = Dataset_results2['local']
           
           plot_df(Dataset_results2, x=Dataset_results2.utc, y=Dataset_results2.value, title='Air Quality for ' + Test_results_location[0] + " by " + Test_Parameter[0])    
           #print(Dataset_results2.index)
                   
           #print("Dataframe shape: ", Dataset_results2.shape)

           dt = pd.Series(Dataset_results2.index[-1] - Dataset_results2.index[0]).view(np.int64)/1e9
           #print(dt)
   #        dt1 = (Dataset_results2.index[-1] - Dataset_results2.index[0]).astype('timedelta64[h]')     
    #       print(dt1)
           #dt = (Dataset_results2.index[-1] - Dataset_results2.index[0])
           dt2 = pd.Timedelta(Dataset_results2.index[-1] - Dataset_results2.index[0]).seconds / 3600.0
           #print(dt2)
           #print(Dataset_results2.index[-1])
           #print(Dataset_results2.index[0])
           
           #print(len(Dataset_results2.index))
           #print(len(Test_Parameter[2]))
           #print(len(Test_Parameter[3]))
           #print(Test_Parameter[3])
           #print(Dataset_results2)
        #   print(dt) 
         #  print("Number of hours between start and end dates: ", dt / np.timedelta64(1, 's'))

           

print("End")    

#print("Dataframe shape: ", df.shape)
#dt = (df.index[-1] - df.index[0])
#print("Number of hours between start and end dates: ", dt.total_seconds()/3600 + 1)



