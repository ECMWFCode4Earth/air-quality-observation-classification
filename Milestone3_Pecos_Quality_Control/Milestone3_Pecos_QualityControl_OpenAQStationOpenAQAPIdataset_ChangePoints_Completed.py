# -*- coding: utf-8 -*-
"""
Created on Wed Nov  4 14:52:17 2020

@author: wegia
"""




import openaq

import pandas as pd

import pecos

from pandas.io.json import json_normalize

import matplotlib.pyplot as plt

from datetime import datetime, date, time, timezone

import numpy as np

import eia

import changefinder

import ruptures as rpt


def Milestone1_Get_OpenAQStation_Latlng(OpenAQStationCountry):
    
    
   OpenAQLatLng = api.locations(location=OpenAQStationCountry, df=True)

   OpenAQLatlngDataset = []


   print(OpenAQLatLng)
   
   OpenAQLatlngDataset.append(OpenAQLatLng['coordinates.latitude'])
 
   OpenAQLatlngDataset.append(OpenAQLatLng['coordinates.longitude'])

   return OpenAQLatlngDataset


def Milestone1_Get_OpnenAQ_Dataset_Measurement_perStation(StationOpenAQ, parameter):
    
#Step 1 Choose the measurement country to import and parameter 
    
   res1 = api.measurements(location=StationOpenAQ, parameter=parameter, date_to=dt_end, date_from=dt_begin, limit=10000, df=True)

   print("Completed measurements ")

   return res1



def Milestone2_Get_OpenAQ_Dataset_Wrangling_utc_index(OpenAQ_Dataset_ImportAPI):

   format = '%Y-%m-%d %H:%M:%S'
    
   OpenAQ_Dataset_ImportAPI['date.utc'] = pd.to_datetime(OpenAQ_Dataset_ImportAPI['date.utc'], format=format).dt.tz_localize(None)

   OpenAQ_Dataset_ImportAPI = OpenAQ_Dataset_ImportAPI[OpenAQ_Dataset_ImportAPI.value != -999.00]

   Formating = pd.DatetimeIndex(OpenAQ_Dataset_ImportAPI['date.utc'])
                 
 
   
   OpenAQ_Dataset_ImportAPI = OpenAQ_Dataset_ImportAPI.set_index(Formating)

  # OpenAQ_Dataset_ImportAPI = OpenAQ_Dataset_ImportAPI.set_index('date.utc')

  # print(OpenAQ_Dataset_ImportAPI)

 #  print(OpenAQ_Dataset_ImportAPI['value'])

  # print(OpenAQ_Dataset_ImportAPI['date.utc'])


 #  print(OpenAQ_Dataset_ImportAPI['value'])

   return OpenAQ_Dataset_ImportAPI
   


def Milestone2_Remove_neg_attribute(OpenAQ_Dataset_ImportAPI):
    
    OpenAQ_Dataset_ImportAPI = OpenAQ_Dataset_ImportAPI[OpenAQ_Dataset_ImportAPI.value != -999.00]

    return OpenAQ_Dataset_ImportAPI

def Milestone2_Remove_negative_attribute(OpenAQ_Dataset_ImportAPI):
    
    OpenAQ_Dataset_ImportAPI = OpenAQ_Dataset_ImportAPI[OpenAQ_Dataset_ImportAPI.value >= 0]

    return OpenAQ_Dataset_ImportAPI


def Milestone2_OpenAQ_Dataset_VisualAnalytics_Histogram(df4, parameter, title="", xlabel='Value', ylabel='Amount of Measurements', dpi=100):
    
# Step Create a Histogram of the OpenAQ Dataset for parameter
   
   print("Histrgram of OpenAQ Dataset from OpenAQ API download") 
    
   plt.gca().set(title=title, xlabel=xlabel, ylabel=ylabel)
   
   plt.hist(df4['value'], bins=np.arange(1,df4['value'].max()))
   plt.show()


def Milestone2_Import_OpenAQ_CSV_plot(df4, xaxis, yaxis, parameter, title="", xlabel='Date', ylabel='Value', dpi=100):
    
    
    
    print("OpenAQ Dataset LinePlot")
     
    plt.figure(figsize=(16,5), dpi=dpi)
    plt.plot(xaxis, yaxis, color='tab:blue')
    plt.gca().set(title=title, xlabel=xlabel, ylabel=ylabel)
   
    plt.show()

def Milestone3_Pecos_Complete_QualityControl_One_OpenAQStation(OpenAQStation, OpenAQStation_Dataset, iteration_OpenAQStations):

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
   
   HigherBound = 200 # Edit

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
 
   print("Criteria 3 : Stagnant Measurements ")

   Increment_Increase = 20 # Edit
   
   Increment_Decrease = None # Edit
  
   pm.check_increment([None, 20], key='value') 

   print("Increment Increase")
   
   print(Increment_Increase)

   print("Increment Decrease")
   
   print(Increment_Decrease)


   pm.check_outlier([None, 3], window=12*3600)

   # Step 9 Compute the quality control index for value
   mask = pm.mask[['value']]
   QCI = pecos.metrics.qci(mask)

   print("*****")

   print("OpenAQ Dataset Results ")

   print("Mask")
  
   print(mask) 
   
   print("Performance Metrics")

   print(QCI)

   custom = 'custom' + iteration_OpenAQStations + '.png'

   MeasurementOpenAQ = int(OpenAQStation['value'].max())

   print(OpenAQStation['value'].describe())
  
  # Step 10 Generate graphics
   test_results_graphics = pecos.graphics.plot_test_results(pm.df, pm.test_results)
   OpenAQStation.plot(y='value', ylim=[0,MeasurementOpenAQ], figsize=(7.0,3.5))
   plt.savefig(custom, format='png', dpi=500)

   print(pm.test_results)

   # Step 11 Write test results and report files to test_results.csv and monitoringreport.html

   Report = 'test_results' + OpenAQStation_Dataset + iteration_OpenAQStations + '.csv' 

   MonitoringReport = 'MonitoringReport' + OpenAQStation_Dataset + iteration_OpenAQStations + '.html'

   pecos.io.write_test_results(pm.test_results,filename=Report)
   pecos.io.write_monitoring_report(pm.df, pm.test_results, test_results_graphics, 
                                 [custom], QCI,filename=MonitoringReport)

   return pm.test_results

    
OpenAQdatasetsLatLng = []


def Milestone4_Get_NearestHighway_OpenAQStations(OpenAQLatlng):
  
   OpenAQ_Dataset_LatlngCSV_Download = "OpenAQLatlngNearestHighway.csv"
     
  # df4 = pd.read_csv(OpenAQ_Dataset_LatlngCSV_Download)

 #  df4 = df4.transpose()

   OpenAQStation_NearestDistance = 0;

   #print(df4)

   import csv
   delimiterOpenAQ = ','
   with open(OpenAQ_Dataset_LatlngCSV_Download,'r') as dest_f:
    data_iter = csv.reader(dest_f, delimiter=delimiterOpenAQ)
    
    for dataset in data_iter:
       OpenAQdatasetsLatLng.append(dataset)
     #  print(dataset)
       
    OpenAQDataset = np.asarray(OpenAQdatasetsLatLng)
   
  # print(OpenAQDataset)
   
   for OpenAQStationLatlng in OpenAQdatasetsLatLng[0]:
   
    #  print(" OpenAQ ")
      
    #  print(OpenAQStationLatlng)
 #     print(OpenAQLatlng[0])
      
      OpenAQStationDatasetLatlng = OpenAQStationLatlng.split('?')
     
    #  print(OpenAQStationDatasetLatlng)   
      if(float(OpenAQStationDatasetLatlng[0]) == float(OpenAQLatlng[0])):
          if(float(OpenAQStationDatasetLatlng[1]) == float(OpenAQLatlng[1])):
            OpenAQStation_NearestDistance = OpenAQStationDatasetLatlng
  #          print(OpenAQStationLatlng[0])
   #         print(OpenAQLatlng[0])
      
   print(OpenAQStation_NearestDistance)
   print(OpenAQLatlng[0])
   print(OpenAQLatlng[1])
   
   
   
   return OpenAQStation_NearestDistance

def Milestone6_Get_Trends_Measurements(OpenAQDataset):
    
   OpenAQDatasetnp = np.array(OpenAQDataset)
    
   print(OpenAQDatasetnp)
   
   electro = OpenAQDatasetnp 
      
   #API
   
   OpenAQdataset = electrocardiogram()[2000:4000]

   print(OpenAQdataset) 
   print(type(electro))
   peaks, _ = find_peaks(OpenAQDatasetnp, height=1.5)
   plt.plot(electro)
   
   print(peaks)
   plt.plot(peaks, electro[peaks], "x")
   
   plt.show()
   
   plt.plot(np.zeros_like(electro), "--", color="gray")
   plt.show()

   border = np.sin(np.linspace(0, 100 * np.pi, electro.size)) 
   
   print(border * 10)
   peaks, _ = find_peaks(electro, height=(-border, border))
   plt.plot(electro)
   
   plt.show()
   plt.plot(-border, "--", color="gray")
   plt.plot(border, ":", color="gray")
   plt.show()
   plt.plot(peaks, electro[peaks], "x")
   plt.show()


   peaks, properties = find_peaks(electro, prominence=(None, 0.6))
#   properties["prominences"].max()
  # 0.5049999999999999
   plt.plot(electro)
   plt.plot(peaks, electro[peaks], "x")
   plt.show()





print("Get the OpenAQ measurements for one chosen OpenAQ and doing Quality Control on it")

#Step 1 Choose the measurement country to import and parameter
#
# Choose the station
#
# OpenAQStationCountry = ''


print("  STEP 1 ")

print("********")

print("Chosen OpenAQ Station: ")
     
OpenAQStationCountry = 'US Diplomatic Post: Abu Dhabi'


OpenAQStationdfDatasetCountry = 'US Diplomatic Post Abu Dhabi'

print(OpenAQStationCountry)

# Step 2 Choose parameter

print("  STEP 2 ")

print("********")


print("Parameter chosen")

parameter = 'pm25'

print(parameter)


#Step 3 Choose time schedule 
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

# dt_start = date.today()

print("  STEP 3 ")

print("********")


print("Getting OpenAQ dataset applying pyOpenAQ API from ") 
print(dt_begin)
print(" to ")
print(dt_end)
print(" for one OpenAQ Station and one parameter ")

# Step 4 Inituial pyOpen API 
#
#  1 There are no edits 

print("  STEP 4 ")

print("********")

print("Initial OpenAQ API")

api = openaq.OpenAQ()

print("OpenAQ pyOpenAPI begun")

# Step 5 Get Measurements from openAQ API 
#
#


#res1 = api.measurements(coordinates=40.23,34.17, df=True, limit=10000)
#resp = api.cities(df=True, limit=10000)

#res1 = api.measurements(city='Delhi', df=True, limit=10000)

print("  STEP 5 ")

print("********")

print("Getting Measurements from OpenAQ API source")

res2 = Milestone1_Get_OpnenAQ_Dataset_Measurement_perStation(OpenAQStationCountry, parameter)

#print(Measurements1)

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
  res2 = Milestone2_Remove_neg_attribute(res2)
  print("Removing missing measurements that are -999.0")
else:
  print("Not removing missing measurements that are -999.0")  
  
if(Remove_Negative_Measurements == Remove_Neg_YES):
  res2 = Milestone2_Remove_negative_attribute(res2)
  print("Removing measurement below 0")
  
  
# Step 7 Do Data Wrangling on OpenAQ dataset  
#
# 1 It convert utc to DateTime for Pecos Quality Control and utc to index
#
#   
  

print("  STEP 7 ")

print("********")
  
print("Data Wrangling OpenAQ dataset evaluating UTC date to Date format and setting utc to index")
  
res2 = Milestone2_Get_OpenAQ_Dataset_Wrangling_utc_index(res2)

print("Dataset Wrangling Completed")

print("OpenAQ Dataset imported ")

print(res2.dtypes)

# Step 8 Import just Measurements to Dataframe with Date utc index for applying 

print("  STEP 8 ")

print("********")

print("Get measurement to Dataframe")
  
OpenAQAPIdataset = pd.DataFrame(res2, columns=['value'])


# Step 10 Completing the Pecos Quality Control 
#
#  1 The Search Criteria are edited in the Method 
#
#  Milestone3_Pecos_Complete_QualityControl_One_OpenAQStation
#
#  2 The iteration can be change to document every time it is processed 
#
#   iteration_OpenAQStations = '0'

#Step 9 Plot OpenAQ Dataset to Line plot and Histogram

print("  STEP 9 ")

print("********")

print("Graph of OpenAQ Dataset Measumrents")


OpenAQDataset_VisualAnalytics = "OpenAQ Dataset Station " + OpenAQStationdfDatasetCountry + " " + parameter + " Time Schedule " + str(dt_begin) + " to " + str(dt_end)

Milestone2_Import_OpenAQ_CSV_plot(OpenAQAPIdataset, OpenAQAPIdataset.index, OpenAQAPIdataset['value'], parameter, title=OpenAQDataset_VisualAnalytics, xlabel='Date UTC', ylabel='Value', dpi=100)

Milestone2_OpenAQ_Dataset_VisualAnalytics_Histogram(OpenAQAPIdataset, parameter, title=OpenAQDataset_VisualAnalytics, xlabel='Value', ylabel='Amount of Measurements', dpi=100)

print("  STEP 10 ")

print("********")

print("Get Pecos Quality Control on OpenAQ dataset")

print("Iteration ")


iteration_OpenAQStations = '0'  #Edit 

print(iteration_OpenAQStations)

print("OpenAQ Pecos Quality Control Search Criteria: ")

print(" **** ")

Milestone3_Pecos_Complete_QualityControl_One_OpenAQStation(OpenAQAPIdataset,  OpenAQStationdfDatasetCountry, iteration_OpenAQStations)

print("  STEP 10 ")

print("********")

print("Get Distance to Nearest Highway")


OpenAQStationLatlng = Milestone1_Get_OpenAQStation_Latlng(OpenAQStationCountry)

OpenAQStationLatlng_NearestHighway = Milestone4_Get_NearestHighway_OpenAQStations(OpenAQStationLatlng)

print(OpenAQAPIdataset['value'].describe())

print("Distance to the nearest Highway in Km ")

print(OpenAQStationLatlng_NearestHighway[4])



# Step 11 

print("  STEP 10 ")

print("********")

print("Get Large increases in Dataset")

# Milestone6_Get_Trends_Measurements(OpenAQAPIdataset['value'])


def retrieve_time_series(api, series_ID):
    """
    Return the time series dataframe, based on API and unique Series ID
    api: API that we're connected to
    series_ID: string. Name of the series that we want to pull from the EIA API
    """
    #Retrieve Data By Series ID 
    series_search = api.data_by_series(series=series_ID)
    ##Create a pandas dataframe from the retrieved time series
    df = pd.DataFrame(series_search)
    return df

if __name__ == "__main__" :
    #Create EIA API using your specific API key
    api_key = '75e8a6cb05e28b0bb25187537e8db309'
    api = eia.API(api_key)
    
    #Pull the oil WTI price data
    series_ID='PET.RWTC.D'
    price_df=retrieve_time_series(api, series_ID)
    price_df.reset_index(level=0, inplace=True)
    #Rename the columns for easer analysis
    price_df.rename(columns={'index':'Date',
            price_df.columns[1]:'WTI_Price'}, 
            inplace=True)
    #Format the 'Date' column 
    price_df['Date']=price_df['Date'].astype(str).str[:-3]
    #Convert the Date column into a date object
    price_df['Date']=pd.to_datetime(price_df['Date'], format='%Y %m%d')
    #Subset to only include data going back to 2014
    price_df=price_df[(price_df['Date']>='2014-01-01')]

    #Convert the time series values to a numpy 1D array
    points=np.array(OpenAQAPIdataset['value'])
    
    
  #  print(points)
    
    #RUPTURES PACKAGE
    #Changepoint detection with the Pelt search method
    model="rbf"
    algo = rpt.Pelt(model=model).fit(points)
    result = algo.predict(pen=10)
    rpt.display(points, result, figsize=(10, 6))
    plt.title('Change Point Detection: Pelt Search Method')
    plt.show()  
    
    #Changepoint detection with the Binary Segmentation search method
    model = "l2"  
    algo = rpt.Binseg(model=model).fit(points)
    my_bkps = algo.predict(n_bkps=10)
    # show results
    rpt.show.display(points, my_bkps, figsize=(10, 6))
    plt.title('Change Point Detection: Binary Segmentation Search Method')
    plt.show()
    
    #Changepoint detection with window-based search method
    model = "l2"  
    algo = rpt.Window(width=40, model=model).fit(points)
    my_bkps = algo.predict(n_bkps=10)
    rpt.show.display(points, my_bkps, figsize=(10, 6))
    plt.title('Change Point Detection: Window-Based Search Method')
    plt.show()
    
    #Changepoint detection with dynamic programming search method
    model = "l1"  
    algo = rpt.Dynp(model=model, min_size=3, jump=5).fit(points)
    my_bkps = algo.predict(n_bkps=10)
    rpt.show.display(points, my_bkps, figsize=(10, 6))
    plt.title('Change Point Detection: Dynamic Programming Search Method')
    plt.show()
    
    #Create a synthetic data set to test against
  #  points=np.concatenate([np.random.rand(100)+5,
                                #     np.random.rand(100)+10,
                                 #    np.random.rand(100)+5])
    
   # print(points)
    
    #CHANGEFINDER PACKAGE
    f, (ax1, ax2) = plt.subplots(2, 1)
    f.subplots_adjust(hspace=0.4)
    ax1.plot(points)
    ax1.set_title("data point")
    #Initiate changefinder function
    cf = changefinder.ChangeFinder()
    scores = [cf.update(p) for p in points]
    ax2.plot(scores)
    ax2.set_title("anomaly score")
   # plt.show()


