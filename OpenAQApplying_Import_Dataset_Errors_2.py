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




print(Dataset[['date','value','parameter','location']])

print(Dataset.dtypes)

#How to split column into two columns
#https://www.geeksforgeeks.org/split-a-text-column-into-two-columns-in-pandas-dataframe/

Dataset[['Dateutc','Datelocal']] = Dataset.date.apply(lambda x: pd.Series(str(x).split(",")))

Dataset_split = Dataset.Dateutc.apply(lambda x: pd.Series(str(x).split(":")))

#print(Dataset_split)

Dataset['utc'] = pd.to_datetime(Dataset_split[1])

#print(Dataset.dtypes)

#print(Dataset)



pd.to_datetime(Dataset['utc'])


Dataset2 = Dataset[['utc','value','parameter','location']].copy()

pd.to_datetime(Dataset2['utc'])
#Dataset2.set_index('utc')

Location_Subset = Dataset[['location']].copy()


Location_Subset.sort_values('location', ascending=False)
Location_Subset = Location_Subset.drop_duplicates(subset='location', keep='first')

#Location_Subset.drop_duplicates('location')

print(Location_Subset)


print(Location_Subset.dtypes)

print(Dataset2.dtypes)

Dataset2.index = Dataset2['utc']

#pd.to_datetime(Dataset2.index)

#LocationId = Dataset2.groupby('location').groups


#plot_df(df, x=Dataset2.index, y=Dataset2.value, title='Monthly anti-diabetic drug sales in Australia from 1992 to 2008.')    

Test_results_location_subset = []


i = 0

pm2 = []

for LocationId in Location_Subset['location']:
 
    print(LocationId)   
  
    Test_results_location_subset_parameter = []
    
    Test_results_location_subset_parameter.append(LocationId)
    
    Dataset3 = Dataset2[Dataset2['location']==LocationId]
    
    
    pd.to_datetime(Dataset3['utc'])
    Test_results_location_subset_parameter_subset = Dataset3[['parameter']].copy() 
         
    #print(Test_results_location_subset_parameter_subset)
    
    Test_results_location_subset_parameter_subset.sort_values('parameter', ascending=False)
    Test_results_location_subset_parameter_subset = Test_results_location_subset_parameter_subset.drop_duplicates(subset='parameter', keep='first')

    for parameter in Test_results_location_subset_parameter_subset['parameter']:
        
        print(parameter)
        
        Test_results_parameter = []
        
        Test_results_parameter.append(parameter)
        
        Dataset4 = Dataset3[Dataset3['parameter']==parameter]      

        Dataset4['year'] = Dataset4['utc'].dt.year
        
        Dataset4['month'] = Dataset4['utc'].dt.month

        Dataset4['day'] = Dataset4['utc'].dt.day
        
        pd.to_datetime(Dataset4['utc'])

        Dataset5 = Dataset4;

        # Initialize logger
        pecos.logger.initialize()

        # Create a Pecos PerformanceMonitoring data object
        pm1 = pecos.monitoring.PerformanceMonitoring()

        pm1.add_dataframe(Dataset4)
        
        pm1.check_missing()
        
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
        

        print(pm1.test_results)
        
        Test_results_parameter.append(len(pm1.test_results))
        
        Test_results_parameter.append(pm1.test_results)
        Test_results_parameter.append(Dataset5)
        
        Test_results_location_subset_parameter.append(Test_results_parameter)
        
        
        
        #i = i + 1
       

    Test_results_location_subset.append(Test_results_location_subset_parameter)
    

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

pm.check_range([0, 1], 'B')
pm.check_range([-1, 1], 'Wave')
pm.check_range([None, 0.25], 'Wave Error')


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
           
           Dataset_results2 = Dataset[Dataset['parameter']==Test_Parameter[0]] 
             
           
           print(Test_results_location[0])
           print(Test_Parameter[0])
           print(Test_Parameter[2])  
           pd.to_datetime(Dataset_results2['utc'])
           #print(Dataset_results2['utc'].dt.year) 
           #print(Dataset_results2['utc'].dt.month)
           #print(Dataset_results2['utc'].dt.day)
           #print(Dataset_results2)
           
           Dataset_results2.index = Dataset_results2['utc']
           
           plot_df(Test_Parameter[3], x=Test_Parameter[3].index, y=Test_Parameter[3].value, title='Air Quality for ' + Test_results_location[0] + " by " + Test_Parameter[0])    
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
           
           print(len(Dataset_results2.index))
           print(len(Test_Parameter[2]))
           
           print(len(Test_Parameter[3]))
           print(Test_Parameter[3])
           print(Dataset_results2)
        #   print(dt) 
         #  print("Number of hours between start and end dates: ", dt / np.timedelta64(1, 's'))

           

print("End")    

#print("Dataframe shape: ", df.shape)
#dt = (df.index[-1] - df.index[0])
#print("Number of hours between start and end dates: ", dt.total_seconds()/3600 + 1)



