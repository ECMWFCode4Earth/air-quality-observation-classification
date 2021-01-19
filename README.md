# air-quality-observation-classification
  
air-quality-observation-classification description 

Validating and removing errors outliers from surface air quality observations from individual sensors so that these observation can be compared to ECMWF's CAMS air quality forecasts. By clustering analysis on these observations more reliable observations can be identified. Enhancing these observations by attaching data about factors that affect air quality these observations can have more credibility about their accuracy. CAMS lacks credible surface air quality observations in many parts of the world, often in the most polluted area such as in India or Africa. Some observations are available for these areas from data harvesting efforts such as openAQ but there is no quality control applied to the data, and it is often not well known if the observations are made in a rural, urban or heavily polluted local environment. This information on the environment is important because the very locally influenced measurements are mostly not representative for the horizontal scale (40 km) of the CAMS forecasts and should therefore not be used for the evaluation of the CAMS model.

# Aims 

1 A Quality Control evaluation of openAQ dataset including Visual Analytics of OpenAQ Stations 

2 Find Outliers and Errors in OpenAQ Measurements 

3 Determine Reliability of OpenAQ Stations 

4 Allowing further analysis of openAQ dataset

# User Manual 

# Milestone 1

## Step 1 Open Milestone1 

## Step 2 See User Manual and edit OpenAQ dataset parameters 

## Step 3 Processes selected Process 

## Step 4 Copy address of resulting CSV download

# Milestone 2

## Step 1 Open Milestone 2 

## Step 2 See User Manual and change CSV download address to downloaded

## Step 3 Process ""

# Milestone 3

## Step 1 Open Milestone 3

## Step 2 See User Manual and change CSV download address to download

## Step 3 Change Quality Control Search Criteria in YML text file for the parameters i.e. default_03_paramters.yml 

## Step 4 Process ""

## Step 5 View results in Monitoring report for OpenAQ Stations or dashboard of selected OpenAQ stations

# Milestone 4

## Step 1 Open Milestone 3

## Step 2 See User Manual and change CSV download address to download

## Step 3 Process 


# Implementation 

## Milestone1_Importing-datasets-from-OpenAQ

Importing OpenAQ datasets to dataframes

## Milestone2_Identifying_reliable_stations

Data Wrangling on OpenAQ entries 

Visual Analytics on OpenAQ datasets

## Milestone3_Pecos_Quality_Control

Pecos Quality Control evaluation on OpenAQ datasets to find Outliers and Errors

## Milestone4_Classification_of_Stations_attr

Nearest Highway to Station compared to statistics


# Dependencies

1 Pecos for Milestone 3

https://pecos.readthedocs.io/en/latest/installation.html

2 py-OpenAQ for Milestone 1

https://github.com/dhhagan/py-openaq
