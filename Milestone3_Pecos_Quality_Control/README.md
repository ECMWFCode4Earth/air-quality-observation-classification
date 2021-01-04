  
# Air Quality Observations Quality Control  

# Description
Validating and removing errors outliers from surface air quality observations from individual sensors so that these observation can be compared to ECMWF's CAMS air quality forecasts. By clustering analysis on these observations more reliable observations can be identified. Enhancing these observations by attaching data about factors that affect air quality these observations can have more credibility about their accuracy. CAMS lacks credible surface air quality observations in many parts of the world, often in the most polluted area such as in India or Africa. Some observations are available for these areas from data harvesting efforts such as openAQ but there is no quality control applied to the data, and it is often not well known if the observations are made in a rural, urban or heavily polluted local environment. This information on the environment is important because the very locally influenced measurements are mostly not representative for the horizontal scale (40 km) of the CAMS forecasts and should therefore not be used for the evaluation of the CAMS model.

Completed for ECMWF European Centre for Medium Weather Forecast 2020 
and ESoWC 2020

# Features 

1 Search through openAQ dataset to analyse what are high measurements and trends 

2 Choose Search criteria for Pecos Quality Control i.e. higher bound, increment and corrupt values 

3 Process the Pecos Quality control on various openAQ datasets for countries, stations, parameters and 6 months or other 

# Implementation 


## 1 Search OpenAQ dataset 

   Open in a browser to get interface 
 
http://gordonrates.co.uk/Air_Quality/workshop/Apps/F_DATASTORE_A_IMPORT_SubFunct5_Attach_Compt1_AirQuality_Dataset/openaq-browser/src/index2_copy.html

   Choose lastest measurements, locations, countries or other pages 

   Choose Search of openAQ dataset. Use the user manual ECMWF_AQQC_Search_OpenAQ_M3_UserManual.pdf

   Find a high bound for measurements on station, region or parameter

   Scroll down to choose Pecos Search Criteria and enter to selection and submit 
  
## 2 Milestone 3 Pecos Quality Control and choose Pecos Quality Control search criteria 

Process "Milestone3_3_Pecos_QualityControl_Coordinates_OpenAQ_Deployed.py"

## 3 Process Pecos Quality Control analysis 


## 4 Dashboard with performance metric and link to monitoring report


# Aims 

1 Choose an upper bound of values and identify value over to be outliers by searching openAQ dataset

2 Choose a lower bound of values 

3 Choose an increment on measurements that is acceptable for both increasing and decreasing values 

4 Find How many stations don’t measure every 15 minutes through a day and when are these are

5 Find stagnant measurements that don't change over a chosen amount 

# User Manual

## 1 Search OpenAQ Dataset 

ECMWF_AQQC_Search_OpenAQ_M3_UserManual.pdf

## 2 Choose Pecos Quality Control Criteria 

Milestone3_Pecos_QualityControl_Choose_Search_Criteria_UserManual.pdf

## 3 Complete Pecos Quality Control 

Milestone3_UserManual_Pecos_Quality_Control.pdf


# Parameters 

1 Higher bound
2 Lower Bound 
3 Timestep of expected measurements
4 The higher bound and lower bound that designate stagnant measurements  
5 Increment over measurements 

# Presentation results

The scripts output to test_results.csv and monitoring_report.html
(There are examples of these in the github)

# Python Scripts 

 ## 1. The Pecos Quality Control for one OpenAQ Station

"Milestone3_Pecos_QualityControl_OpenAQStationimportOpenAQAPIdataset_Completed.py"

 ## 2. The Pecos Quality Control for station within a coordinate center Latitude and longitude and a radius.

"Milestone3_3_Pecos_QualityControl_Coordinates_OpenAQ_Deployed.py"

# Dependencies

Pecos Package 

https://pecos.readthedocs.io/en/stable/overview.html
https://github.com/sandialabs/pecos

