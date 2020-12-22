# -*- coding: utf-8 -*-
"""
Created on Tue Dec  1 15:12:57 2020

@author: wegia
"""



import pandas as pd

import pecos

import seaborn as sns

from pandas import json_normalize

import matplotlib.pyplot as plt

from datetime import datetime, date, time, timezone

import numpy as np

import csv
    

def Milestone2_Get_OpenAQ_Dataset_Wrangling_utc_index(OpenAQ_Dataset_ImportAPI):

   format = '%Y-%m-%d %H:%M:%S'
    
   OpenAQ_Dataset_ImportAPI['date.utc'] = pd.to_datetime(OpenAQ_Dataset_ImportAPI['date.utc'], format=format).dt.tz_localize(None)

   OpenAQ_Dataset_ImportAPI = OpenAQ_Dataset_ImportAPI[OpenAQ_Dataset_ImportAPI.value != -999.00]

   Formating = pd.DatetimeIndex(OpenAQ_Dataset_ImportAPI['date.utc'])
  
   OpenAQ_Dataset_ImportAPI = OpenAQ_Dataset_ImportAPI.set_index(Formating)

   return OpenAQ_Dataset_ImportAPI
   


def Milestone2_Remove_neg_attribute(OpenAQ_Dataset_ImportAPI):
    
    OpenAQ_Dataset_ImportAPI = OpenAQ_Dataset_ImportAPI[OpenAQ_Dataset_ImportAPI.value != -999.00]

    return OpenAQ_Dataset_ImportAPI

def Milestone2_Remove_negative_attribute(OpenAQ_Dataset_ImportAPI):
    
    OpenAQ_Dataset_ImportAPI = OpenAQ_Dataset_ImportAPI[OpenAQ_Dataset_ImportAPI.value >= 0]

    return OpenAQ_Dataset_ImportAPI

def Milestone2_OpenAQ_Dataset_VisualAnalytics_Histogram_Unique(df4, OpenAQStationunique, xaxis, yaxis, parameter, OpenAQDataset_VisualAnalytics, OpenAQDataset_VisualAnalytics_iteration, xlabel='Value', ylabel='Amount of Measurements', dpi=100):
   
   OpenAQ_Dataset_Graph_df = [] 
    
   for OpenAQunique in OpenAQStationunique:
      
      OpenAQ_Dataset_Graph = []  
       
      OpenAQAPIdatasetunique = df4[df4['location'] == OpenAQunique]
      
      OpenAQDataset_VisualAnalytics_Dataset = OpenAQDataset_VisualAnalytics + " Station OpenAQ " + OpenAQunique
      
      OpenAQ_Dataset_df = Milestone2_OpenAQ_Dataset_VisualAnalytics_Histogram(OpenAQAPIdataset, parameter, OpenAQDataset_VisualAnalytics_iteration + OpenAQunique, title=OpenAQDataset_VisualAnalytics_Dataset, xlabel='Value', ylabel='Amount of Measurements', dpi=100)
      
      OpenAQ_Dataset_Graph.append(OpenAQunique)
      
      OpenAQ_Dataset_Graph.append(OpenAQ_Dataset_df)
      
      OpenAQ_Dataset = Milestone2_Import_OpenAQ_CSV_plot(OpenAQAPIdataset, xaxis, yaxis, parameter, OpenAQDataset_VisualAnalytics_iteration + OpenAQunique, title=OpenAQDataset_VisualAnalytics_Dataset, xlabel='Value', ylabel='Amount of Measurements', dpi=100)

      OpenAQ_Dataset_Graph.append(OpenAQ_Dataset)

      OpenAQ_Dataset_Graph_df.append(OpenAQ_Dataset_Graph)

   return OpenAQ_Dataset_Graph

def Milestone2_Import_OpenAQ_CSV_plot_Unique(df4, OpenAQStationunique, xaxis, yaxis, parameter, OpenAQDataset_VisualAnalytics, xlabel='Value', ylabel='Amount of Measurements', dpi=100):
   
   for OpenAQunique in OpenAQStationunique:
        
      print(OpenAQunique) 
       
      OpenAQAPIdatasetunique = df4[df4['location'] == OpenAQunique]
      
      Milestone2_Import_OpenAQ_CSV_plot(OpenAQAPIdataset, xaxis, yaxis, parameter, OpenAQ_Dataset, title=OpenAQDataset_VisualAnalytics, xlabel='Value', ylabel='Amount of Measurements', dpi=100)


def Milestone2_OpenAQ_Dataset_VisualAnalytics_Histogram(df4, parameter, OpenAQDataset_VisualAnalytics_iteration, title="", xlabel='Value', ylabel='Amount of Measurements', dpi=100):
    
# Step Create a Histogram of the OpenAQ Dataset for parameter
   
   print("Histogram of OpenAQ Dataset from OpenAQ API download") 
    
   plt.gca().set(title=title, xlabel=xlabel, ylabel=ylabel)
   
   plt.hist(df4['value'], bins=np.arange(1,df4['value'].max()))
   
   OpenAQ_Dataset = OpenAQDataset_VisualAnalytics_iteration + " Histogram" + ".png"
   
   
   plt.savefig(OpenAQ_Dataset)
   
   plt.show()

   return OpenAQ_Dataset


def Milestone2_Import_OpenAQ_CSV_plot(df4, xaxis, yaxis, parameter, OpenAQDataset_VisualAnalytics_iteration,  title="", xlabel='Date', ylabel='Value', dpi=100):
    
   print("OpenAQ Dataset LinePlot")
     
   plt.figure(figsize=(16,5), dpi=dpi)
   plt.plot(xaxis, yaxis, color='tab:blue')
   plt.gca().set(title=title, xlabel=xlabel, ylabel=ylabel)
   
    
   OpenAQ_Dataset = OpenAQDataset_VisualAnalytics_iteration + " Line Graph" + ".png"
    
    
   plt.savefig(OpenAQ_Dataset)
 
   plt.show()

   return OpenAQ_Dataset



def Milestone3_Get_Imported_OpenAQ_Dataset_parameter_unique_Test(OpenAQDatasetparameter, TestId, Test_Analysis):
    
   OpenAQStationparameter = OpenAQDatasetparameter['parameter'].unique()

   if(len(OpenAQStationparameter) == 0):
     parameter = OpenAQStationparameter[0]
  
   else:
     parameter = Parameter_Default  
    
     
   return parameter
   
def Milestone3_Get_Imported_OpenAQ_Dataset_Test(OpenAQ_Dataset_OpenAQCSV_Download_Test, TestId, Test_Analysis):
    
   Milestone3_Get_Imported_OpenAQ_Dataset(OpenAQ_Dataset_OpenAQCSV_Download_Test)
    



def Milestone3_Get_VisualAnalytics(OpenAQDataset, OpenAQStation):
     
    OpenAQdfDataset = []
    
    
    for OpenAQdatasetGraph in OpenAQDataset:
      
       if(OpenAQdatasetGraph[0] == OpenAQStation): 

           OpenAQdfDataset = OpenAQdatasetGraph
           
    return OpenAQdfDataset       
           
def Milestone3_Pecos_Complete_QC_QualityControl_OpenAQStation(OpenAQStation, OpenAQDataset_VisualAnalytics_iteration, OpenAQStationunique, OpenAQDataset):
    
    
   for OpenAQunique in OpenAQStationunique:
        
      print(OpenAQunique) 
       
      OpenAQAPIdatasetunique = OpenAQStation[OpenAQStation['location'] == OpenAQunique]
      
      OpenAQCompleteDataset = Milestone3_Get_VisualAnalytics(OpenAQDataset, OpenAQunique)
      
      Milestone3_Pecos_Complete_QualityControl_One_OpenAQStation(OpenAQStation, OpenAQDataset_VisualAnalytics_iteration, OpenAQDataset) 

def Milestone3_Pecos_Complete_QualityControl_One_OpenAQStation(OpenAQStation, OpenAQDataset_VisualAnalytics_iteration, OpenAQDataset):

   # Step 2 Initialize logger and Create a Pecos PerformanceMonitoring data object
   pecos.logger.initialize()
 
   pm = pecos.monitoring.PerformanceMonitoring()


   # Step 3 Append Dataframe to Pecos PerformanceMonitoring data object
   pm.add_dataframe(OpenAQStation)


   # Step 4 Check the expected frequency of the timestamp
   #
   # 1 Edit timestep when 900 is 15 mins     



   Timestep = 900 # Edit
   
   pm.check_timestamp(Timestep)

   print("*****")

   print("Criteria 1 : Timestep ")
   
   print(Timestep)
   
  
   # Step 5 Check for missing data
   pm.check_missing()
   
# Step 6 Choose acceptable value range and Check data for expected ranges
#
# Parameters
#  
#  1 Lower bound of values
#  2 Higher Bound of values
#  3 Data column (default = None, which indicates that all columns are used)
#  4 Minimum number of consecutive failures for reporting (default = 1)le increment from measurements of 15 minutes and check for abrupt changes between consecutive time steps
#
#   e.g pm.check_range([0, 200], key='value')  
#         pm.check_range([1, 2], key='3',4)
#
# Results: Any value outside of the range is an outlier

   LowerBound = None # Edit 
   
   HigherBound = 400 # Edit

   pm.check_range([LowerBound, HigherBound], key='value')
 

   print("*****")
   
   print("Criteria 2 : Lower Bound and Higher Bound ")
  
   print("Lower Bound ")
   
   print(LowerBound)   
   
   print("Higher Bound")
   
   print(HigherBound)
   
# Step 7 Choose the min amount that is acceptable to change from measurements 
#
# Parameters:
#
#    1 Lower bound to decrease by
#    2 Upper bound to increase by
#    3 Size of the moving window used to compute the difference between the minimum and maximum
#    4 Data column (default = None, which indicates that all columns are used)
#    5 Flag indicating if the test should only check for positive delta (the min occurs before the max) or negative delta (the max occurs before the min) (default = False)
#    6 Minimum number of consecutive failures for reporting (default = 1)

#  e.g. pm.check_delta([Miniumn Decrease, Min Increase], window=3600, 'value')
#      included parametes 1-6: pm.check_delta([1, 2], window=3, key='4', 5, 6)
#
#  Results: When over min decrease or increase it is an outlier
 
   print("*****")
 
   
   print("Criteria 3 : Stagnant Measurements ")
  
   DeltaLowerBound = None # Edit
   
   DeltaHigherBound = 10 # Edit
   
   DeltaTimeSchedule = 3600 # Edit
   
   pm.check_delta([DeltaLowerBound, DeltaHigherBound], window=DeltaTimeSchedule, key='value')

   print(" Measurement that increase by " )
   
   print(DeltaHigherBound )
   
   print("in Time Schedule")
   
   print(DeltaTimeSchedule)

   print("Delta Lower Bound")

   print(DeltaLowerBound)

# Step 8 Choose acceptable increment on measurements 
#
# Parameters
#  
#  1 Lower bound to de increment by
#  2 Higher Bound to increment by
#  3 Data column (default = None, which indicates that all columns are used)
#  4 Increment used for difference calculation (default = 1 timestamp)
#  5 Flag indicating if the absolute value of the increment is used in the test (default = True)
#  6 Minimum number of consecutive failures for reporting (default = 1)
#
# e.g pm.check_increment([None, 20], 'value') 
#    included parametes 1- 4:  pm.check_increment([1, 2], key='3', 4, 5, 6) 
#
# Results: Any measurement that has a larger increment or de increment by choosen value is an outlier

   print("*****")
 
   print("Criteria 4 : Stagnant Measurements ")

   Increment_Increase = 20 # Edit
   
   Increment_Decrease = None # Edit
  
   pm.check_increment([Increment_Decrease, Increment_Increase], key='value') 

   print("Increment Increase")
   
   print(Increment_Increase)

   print("Increment Decrease")
   
   print(Increment_Decrease)

   print("*****")

   print("Criteria 5: Outlier")
   
   print("UpperBound")

   UpperBoundOutlier = 3 # Edit
   
   print(UpperBoundOutlier)
   
   print("Time Schedule")
     
   TimeSchedule = 12*3600 # Edit
   
   print(TimeSchedule)
   
   pm.check_outlier([None, UpperBoundOutlier], window=TimeSchedule, key='value')

   # Step 9 Compute the quality control index for value
   mask = pm.mask[['value']]
   
  
   
   QCI = pecos.metrics.qci(mask)

   print("*****")

   print("OpenAQ Dataset Results ")

   print("Mask")
  
   print(pm.mask) 
   
 #  print(pm.cleaned_data[pm.cleaned_data['value'] == 'NaN'])
   
   print("Performance Metrics")

   print(QCI)

   custom = 'custom' + iteration_OpenAQStations + '.png'

   custom_graphics_graph = '.png' 

   MeasurementOpenAQ = int(OpenAQStation['value'].max())

   print(OpenAQStation['value'].describe())
  
   
   test_results_graphics_OpenAQ = [] 
   
   # Step 10 Generate graphics
   test_results_graphics = pecos.graphics.plot_test_results(pm.df, pm.test_results)
   
   test_results_graphics_OpenAQ.append(test_results_graphics)
   
   test_results_graphics_OpenAQ.append(OpenAQDataset[1])
   
   test_results_graphics_OpenAQ.append(OpenAQDataset[2])
   
   OpenAQStation.plot(y='value', ylim=[0,MeasurementOpenAQ], figsize=(7.0,3.5))
   plt.savefig(custom, format='png', dpi=500)

   print(pm.test_results)

   # Step 11 Write test results and report files to test_results.csv and monitoringreport.html

   Report = 'test_results' + OpenAQDataset_VisualAnalytics_iteration  + ' Result' + '.csv' 

   MonitoringReport = 'MonitoringReport ' + OpenAQDataset_VisualAnalytics_iteration + '.html'

   pecos.io.write_test_results(pm.test_results,filename=Report)
   pecos.io.write_monitoring_report(pm.df, pm.test_results, test_results_graphics_OpenAQ, 
                                 [custom], QCI,filename=MonitoringReport)
 
   metricsOpenAQ = Milestone3_Get_OpenAQresults(pm.test_results, pm.df, QCI)   
   
   OpenAQDataset_VisualAnalytics_Results.append(Report)
   
   OpenAQDataset_VisualAnalytics_Results.append(MonitoringReport)
   
   OpenAQDataset_VisualAnalytics_Results.append(OpenAQDataset_VisualAnalytics_iteration + 'metrics_file.csv')
    

   pecos.io.write_metrics(metricsOpenAQ, OpenAQDataset_VisualAnalytics_iteration + 'metrics_file.csv') 

   return pm.test_results

def Milestone3_Get_Imported_OpenAQ_DatasetOutlier(OpenAQ_QC_Dataset):
    
   Delta = "Check for stagnant data and/or abrupt changes in the data using the difference between max and min values (delta) within a rolling window"
      
   UpperBound = "Check for data that is outside expected range and Upper Bound"
   
   LowerBound = "Check for data that is outside expected range for Lower Bound"
   
   Increment = "Check data increments using the difference between values"

   Timestamp = "Check time series for missing, non-monotonic and duplicate timestamps"
   
   Outlier = "Check for outliers using normalized data within a rolling window The upper and lower bounds are specified in standard deviations. Data normalized using (data-mean)/std."
   
   FunctionModel = "Analyse"
   
   NotComplete = "Check for missing data"
    
   QCI = "QCI "
   
   
   if(OpenAQ_QC_Dataset == 0):

       print("Criteria 1 Time Stamp")
       
       print(Timestamp)

       print("Criteria 2 Upper Lower Bound")

       print(UpperBound)
       
       print(LowerBound)
       
       print("Criteria 3 Delta ")

       print(Delta)
       
       print("Criteria 4 Increment")

       print(Increment)
       
       print("Criteria 5 Outlier")

       print(Outlier)
       
       print("Criteria 6 Model Function")

       print(FunctionModel)
       
       print("Criteria 7 Missing Dataset")

       print(NotComplete)
   
       print("Performance Metric QCI ")

       print(QCI)
    
    
def Milestone3_Get_Imported_OpenAQ_Dataset(OpenAQDatasetSelect): 
    
   OpenAQ_Dataset_LatlngCSV_Download = '../Milestone1_Importing-datasets-from-OpenAQ/'
   
   OpenAQ_Dataset_LatlngCSV_Download = OpenAQ_Dataset_LatlngCSV_Download + OpenAQDatasetSelect
   
   ImportOpenAQimported = pd.read_csv(OpenAQ_Dataset_LatlngCSV_Download) 
   
   print(ImportOpenAQimported['parameter'])
   
   
   return ImportOpenAQimported 




def Milestone3_Get_Imported_OpenAQ_Dataset_OpenAQDataset_Test(): 
    
   OpenAQ_Dataset_LatlngCSV_Download = '../Milestone1_Importing-datasets-from-OpenAQ/OpenAQ_Dataset1pm25Country2018-03-01to2020-09-01.csv'
       
   ImportOpenAQimported = pd.read_csv(OpenAQ_Dataset_LatlngCSV_Download)
    
   print(ImportOpenAQimported['parameter'])
   

   return ImportOpenAQimported 


def Milestone3_Get_OpenAQresults(OpenAQDFResults, OpenAQDataset, QCI):
    
  
   OpenAQappend = [] 

   OpenAQmetric = []

   for Outlier, df in OpenAQDFResults.groupby('Error Flag'):

     
      print(Outlier)   
    
      print(len(df))
    
      OpenAQappend.append(len(df)) 
      
      OpenAQappend.append(str(Outlier))
     
   OpenAQappend.append("QCI") 
    
 
   OpenAQappend.append(QCI.value)
   
   
   OpenAQDatsetappend = pd.DataFrame(OpenAQappend)
        
   return OpenAQDatsetappend 



OpenAQDataset_VisualAnalytics_Results = []

# Step 1 Get Measurements from openAQ API 
#
#  1 Change the OpenAQ dataset CSV to latest downloaded from Milestone 1 Using Cooridnate and Radius 
#
#    Change OpenAQDatasetSelected to OpenAQ Dataset 
#
#    The address is printed out after completing Milestone 1 Process
#
#  2 Add unique iteration 
#   
#    
#    Add in Coordinates and Radius
#       
#
#  Limitations
#
#   It must be the OpenAQ Dataset downloaded using Coordinate and Radius 
#
#  Test 
#
#
#  OpenAQDatasetSelected_Test = 'OpenAQ_Dataset Unique selection pm25 CoordinateCentreandRadius 2020-03-01 to 2020-09-01.csv'
#
#  Milestone3_Get_Imported_OpenAQ_Dataset_Test(OpenAQDatasetSelected_Test, 1, "Test Coordindate")

print("  STEP 1 ")

print("********")

print("Getting Measurements from OpenAQ API source imported in Milestone 1 from Coordinate and Radius")


#### Edit 

OpenAQDatasetSelected = 'OpenAQ_Dataset Unique selection pm25 CoordinateCentreandRadius 2020-03-01 to 2020-09-01.csv'

ImportedOpenAQimport = Milestone3_Get_Imported_OpenAQ_Dataset(OpenAQDatasetSelected)


print("Choosen Unique Iteration ")

iteration_OpenAQStations = '0'  #Edit 

print(iteration_OpenAQStations)

print("Chosen OpenAQ Coordinates and Radius: ")
     
OpenAQStationCountry = "24.4244,54.43375" #Edit

Radius = 25000 # Edit in metres 

print("Completed Step 1 ")

print(">")


print("  STEP 2 ")

print("********")

print("OpenAQ Dataset imported ")

print(OpenAQDatasetSelected)

print(ImportedOpenAQimport.dtypes)


print("Completed Step 2 ")

print(">")

print("  STEP 3 ")

print("********")


print("Found these Stations from Coordinates")

OpenAQStationunique = ImportedOpenAQimport['location'].unique()

print(OpenAQStationunique)



print("Completed Step 3 ")

print(">")


print("  STEP 4 ")

print("********")

# Step 4 Find the parameter of OpenAQ Dataset
#
#  1 Edit to default parameter if not in OpenAQ dataset
#
# Test 
#
#  1 That is only one parameter 
# 
#
print("Parameter")

Parameter_Default = 'pm25' # Edit

parameter = Milestone3_Get_Imported_OpenAQ_Dataset_parameter_unique_Test(ImportedOpenAQimport,1,"Test unique parameter")

print(parameter)

print("Completed Step 4 ")

print(">")

#Step 5 Finding time schedule 
#
# 
# 1 Change default Time Schedule from 6 months to other in dt_begin
#  and dt_end
#
#  dt_begin =  date(2020,3,1) 1 March 2020 
#
#  dt_end =  date(2020,9,1) 1 September 2020
#
# Change these
#
# dt1begin = date(2020,3,1) # Edit
#
# dt1end = date(2020,9,1) # Edit
#
# dt_begin = dt1begin
#
# dt_end = dt1end

print("  STEP 5 ")

print("********")

dt_begin = min(ImportedOpenAQimport['date.utc'])

dt_end = max(ImportedOpenAQimport['date.utc'])


print(dt_begin)
print(" to ")
print(dt_end)
print(" for one OpenAQ Stations and one parameter ")


print("Completed Step 5 ")

print(">")

# Step 6 Choose to remove measurement that have -999.00
#
# 1 It only removes -999.0 that are missing measurements 
#
#  Edit the Remove_Neg to either
#
#   1 - Remove -999.0 from dataset 
# 
#   0 - Don't remove -999.0 from dataset
#
#  i.e Change to chosen
# 
#   Remove_Neg = 1
#
#  2 Choose to remove negative measurements 
#
#  Change  Remove_Negative_Measurements
#  
#   1 - Remove negative measurements 


print("  STEP 6 ")

print("********")

print("Choose to remove missing measurements that are -999.0 and below 0")

Remove_Neg = 1 # Edit      Removes Only measurements of -999.0 

Remove_Negative_Measurements = 1 # Edit Remove measure below 0 

Remove_Neg_NO = 0

Remove_Neg_YES = 1

if(Remove_Neg == Remove_Neg_YES):
  ImportedOpenAQimport = Milestone2_Remove_neg_attribute(ImportedOpenAQimport)
  print("Removing missing measurements that are -999.0")
else:
  print("Not removing missing measurements that are -999.0")  
  
if(Remove_Negative_Measurements == Remove_Neg_YES):
  ImportedOpenAQimport = Milestone2_Remove_negative_attribute(ImportedOpenAQimport)
  print("Removing measurement below 0")
  
  

print("Completed Step 6 ")

print(">")

# Step 7 Do Data Wrangling on OpenAQ dataset  
#
# 1 It convert utc to DateTime for Pecos Quality Control and utc to index
#
#   
  

print("  STEP 7 ")

print("********")
  
print("Data Wrangling OpenAQ dataset evaluating UTC date to Date format and setting utc to index")

ImportedOpenAQimport = Milestone2_Get_OpenAQ_Dataset_Wrangling_utc_index(ImportedOpenAQimport)
  

print("Dataset Wrangling Completed")

print("OpenAQ Dataset imported ")

print(ImportedOpenAQimport.dtypes)



print("Completed Step 7 ")

print(">")

# Step 8 Import just Measurements to Dataframe with Date utc index for applying 

print("  STEP 8 ")

print("********")

print("Get measurement to Dataframe")

OpenAQAPIdataset = pd.DataFrame(ImportedOpenAQimport, columns=['value','location','unit'])

print("Completed Step 8 ")

print(">")



#Step 9 Plot OpenAQ Dataset to Line plot and Histogram

print("  STEP 9 ")

print("********")

print("Graph of OpenAQ Dataset Measumrents")

OpenAQ_unit = str(ImportedOpenAQimport['unit'][0]) 

OpenAQDataset_VisualAnalytics = "OpenAQ Dataset Station " + " " + parameter + " Time Schedule " + str(dt_begin) + " to " + str(dt_end)

OpenAQDataset_VisualAnalytics_iteration = "OpenAQ Dataset Station " + " " + parameter + " iteration " + iteration_OpenAQStations

OpenAQDataset = Milestone2_OpenAQ_Dataset_VisualAnalytics_Histogram_Unique(OpenAQAPIdataset, OpenAQStationunique, OpenAQAPIdataset.index, OpenAQAPIdataset['value'], parameter, OpenAQDataset_VisualAnalytics, OpenAQDataset_VisualAnalytics_iteration, xlabel='Value', ylabel='Amount of Measurements', dpi=100)

print("Completed Step 9 ")

print(">")


# Step 10 Completing the Pecos Quality Control 
#
#  1 The Search Criteria are edited in the Method 
#
#  Milestone3_Pecos_Complete_QualityControl_One_OpenAQStation
#
#  2 The iteration can be change to document every time it is processed 
#
#   iteration_OpenAQStations = '0'

print("  STEP 10 ")

print("********")

print("Get Pecos Quality Control on OpenAQ dataset")


print("OpenAQ Pecos Quality Control Search Criteria: ")


Milestone3_Pecos_Complete_QC_QualityControl_OpenAQStation(ImportedOpenAQimport, OpenAQDataset_VisualAnalytics_iteration, OpenAQStationunique, OpenAQDataset)

print(" **** ")

OpenAQ_QC_Dataset = 0

Milestone3_Get_Imported_OpenAQ_DatasetOutlier(OpenAQ_QC_Dataset)

print(" Results in Monitoring report")

print(OpenAQDataset_VisualAnalytics_Results)

print("Completed Step 10")

print(">")
