  
# Air Quality Observations Quality Control  

Description
Validating and removing errors outliers from surface air quality observations from individual sensors so that these observation can be compared to ECMWF's CAMS air quality forecasts. By clustering analysis on these observations more reliable observations can be identified. Enhancing these observations by attaching data about factors that affect air quality these observations can have more credibility about their accuracy. CAMS lacks credible surface air quality observations in many parts of the world, often in the most polluted area such as in India or Africa. Some observations are available for these areas from data harvesting efforts such as openAQ but there is no quality control applied to the data, and it is often not well known if the observations are made in a rural, urban or heavily polluted local environment. This information on the environment is important because the very locally influenced measurements are mostly not representative for the horizontal scale (40 km) of the CAMS forecasts and should therefore not be used for the evaluation of the CAMS model.

Completed for ECMWF European Centre for Medium Weather Forecast 2020 
and ESoWC 2020

# Implementation 

Milestone 3 Classification of AQ Stations 

Aims 
1 Import OpenAQ dataset from many sources i.e. csv, ndjson or through api 
2 Import latest measurements for chosen OpenAQ stations
3 Import measurements for 6 months for choosen OpenAQ stations  
4 Import measurements for 18 months for choosen OpenAQ stations
5 Import measurements for every OpenAQ station and parameter

# User Manual

UserManual_Milestone_3_Pecos_Quality_Control_Classification_of_Stations.pdf
(This is for Milestone3_Pecos_Importing_OpenAQ_API_Dataset_Classification_of_Measurements.py)


Parameters 
1 Higher bound
2 Lower Bound 
3 Timestep of expected measurements
4 The higher bound and lower bound that designate stagnant measurements  
5 Increment over measurements 

Python Scripts 

1 
2 Milestone3_Pecos_Importing_OpenAQ_API_Dataset_Classification_of_Measurements.py

2 Milestone3_Pecos_Importing_OpenAQ_API_Dataset_Classification_of_Measurements.py

A Script for importing OpenAQ dataset for One country and one parameter 

1 Milestone3_Pecos_6Month_Importing_OpenAQ_API_Dataset_Classification_of_Measurements_6Months.py

A Script to get 6 Months of OpenAQ dataset from one station and one parameter. The defaults are parameter pm25 and station US Diplomatic Post: Hyderabad 

Parameters: 



# Dependencies

Numpy 

Pandas 

openAQ
