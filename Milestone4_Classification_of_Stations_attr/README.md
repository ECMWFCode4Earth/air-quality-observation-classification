# Air Quality Observations Quality Control

# Description
Validating and removing errors outliers from surface air quality observations from individual sensors so that these observation can be compared to ECMWF's CAMS air quality forecasts. By clustering analysis on these observations more reliable observations can be identified. Enhancing these observations by attaching data about factors that affect air quality these observations can have more credibility about their accuracy. CAMS lacks credible surface air quality observations in many parts of the world, often in the most polluted area such as in India or Africa. Some observations are available for these areas from data harvesting efforts such as openAQ but there is no quality control applied to the data, and it is often not well known if the observations are made in a rural, urban or heavily polluted local environment. This information on the environment is important because the very locally influenced measurements are mostly not representative for the horizontal scale (40 km) of the CAMS forecasts and should therefore not be used for the evaluation of the CAMS model.

Completed for ECMWF European Centre for Medium Weather Forecast 2020 and ESoWC 2020

# Features

1 Get Distance to Nearest Highway from OpenAQ stations

# Implementation

1 Distance to Nearest Highway

openAQ_copy100Latlngattr13000_OpenAQStations.csv

1 - OpenAQ Lat

2 - OpenAQ Lng

3 - PlaceId

4 - Nearest Highway Lat

5 - Nearest Highway Lng

6 - Distance in Km 

2 Get Nearest Highway and Mean of OpenAQ

Process: 

# User Manual 

Step 1 Download Dataset for one AQ Station from the dataset from openAQ.org using Milestone 1

Step 2 Change the csv requested in the  script to chosen OpenAQ Stations 

Other Steps identified in python script 
