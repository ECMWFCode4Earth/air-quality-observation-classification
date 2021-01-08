  
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

When selected OpenAQ dataset by Coordinate Centre and Radius 

Edit Process "Milestone3_3_Pecos_QualityControl_Coordinates_OpenAQ_Deployed.py"

When selected OpenAQ dataset by Choosing OpenAQ station

Edit Process "Milestone3_1_Pecos_QualityControl_OpenAQStation_fromOpenAQAPIdataset.py"

## 3 Results from Pecos Quality Control analysis 

When selected OpenAQ dataset by Coordinate Centre and Radius from Milestone 1 

Process "Milestone3_3_Pecos_QualityControl_Coordinates_OpenAQ_Deployed.py"

The Pecos Quality Control produces these results: 

Monitoring reports for individual OpenAQ Stations

The Outliers and Errors identified in a Excel Spreadsheet for individual OpenAQ Stations

When selected OpenAQ dataset by Choosing OpenAQ station

Process "Milestone3_1_Pecos_QualityControl_OpenAQStation_fromOpenAQAPIdataset.py"

The Pecos Quality Control produces these results: 

A Monitoring report

The Outliers and Errors identified in a Excel Spreadsheet 

# Aims 

## 1 Choose an upper bound of values and identify value over to be outliers by searching openAQ dataset

Quality Control Defininition: "check if data is within expected bounds. i.e. below Upper Bound. Range tests are very flexible. The test can be used to check for expected range on the raw data or using modified data"

## 2 Choose a lower bound of values 

Quality Control Defininition: "check if data is over expected lower bounds. Range tests are very flexible. The test can be used to check for expected range on the raw data or using modified data"

## 3 Choose an increment on measurements that is acceptable for both increasing and decreasing values 

Quality Control Defininition: "check for stagnant data and abrupt changes in data. Checks if the difference between consecutive data values (or other specified increment) is within expected bounds"

## 4 Find how many stations don’t measure every 15 minutes through a day and when these are

Quality Control Defininition: "check the time index for missing, duplicate, and non-monotonic indexes"

## 5 Find stagnant measurements that don't change over a chosen amount 

Quality Control Defininition: "check for stagnant data and abrupt changes in data. The test checks if the difference between the minimum and maximum data value within a moving window is within expected bounds"

## 6 Find outliers due to a test on a selection of measurements. 

Quality Control Definition: "check if normalized data falls outside expected bounds. Data is normalized using the mean and standard deviation, using either a moving window or using the entire data set."

# User Manual

## 1 Search OpenAQ Dataset 

ECMWF_AQQC_Search_OpenAQ_M3_UserManual.pdf

## 2 Choose Pecos Quality Control Criteria 

Milestone3_Pecos_QualityControl_Choose_Search_Criteria_UserManual.pdf

## 3 Complete Pecos Quality Control 

Milestone3_UserManual_Pecos_Quality_Control.pdf


# Parameters 

## Higher Bound

1 Higher bound for OpenAQ Measurements 

## Lower Bound 

2 Lower Bound 

## Timestep 

3 Timestep of expected measurements

## Delta 

4 The higher bound and lower bound that designate stagnant measurements  

## Increment

5 Largest increment over measurements 

## Outlier

6 Outlier high bound over averaged dataset

## Corrupt data

7 Corrupt data

# Presentation results

The scripts output to test_results.csv and monitoring_report.html
(There are examples of these in the github)

## Outliers and Errors

Parameter 1 and 2 Data < lower bound OR Data > upper bound

Parameter 3 Duplicate timestamp or Nonmonotonic timestamp or Missing data (used for missing data and missing timestamp)

Parameter 4 Delta < lower bound OR Delta > upper bound

Parameter 5 Increment < lower bound OR Increment > upper bound

Parameter 6 Outlier < lower bound OR Outlier > upper bound

Parameter 7 Corrupt data 


# Python Scripts 

 ## 1. The Pecos Quality Control for one OpenAQ Station

"Milestone3_1_Pecos_QualityControl_OpenAQStation_fromOpenAQAPIdataset.py"

 ## 2. The Pecos Quality Control for station within a coordinate center Latitude and longitude and a radius.

"Milestone3_3_Pecos_QualityControl_Coordinates_OpenAQ_Deployed.py"

# Dependencies

Pecos Package 

https://pecos.readthedocs.io/en/stable/overview.html
https://github.com/sandialabs/pecos

