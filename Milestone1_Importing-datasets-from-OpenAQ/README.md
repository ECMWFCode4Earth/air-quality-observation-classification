  
# Air Quality Observations Quality Control  

# Description

Validating and removing errors outliers from surface air quality observations from individual sensors so that these observation can be compared to ECMWF's CAMS air quality forecasts. By clustering analysis on these observations more reliable observations can be identified. Enhancing these observations by attaching data about factors that affect air quality these observations can have more credibility about their accuracy. CAMS lacks credible surface air quality observations in many parts of the world, often in the most polluted area such as in India or Africa. Some observations are available for these areas from data harvesting efforts such as openAQ but there is no quality control applied to the data, and it is often not well known if the observations are made in a rural, urban or heavily polluted local environment. This information on the environment is important because the very locally influenced measurements are mostly not representative for the horizontal scale (40 km) of the CAMS forecasts and should therefore not be used for the evaluation of the CAMS model.

Completed for ECMWF European Centre for Medium Weather Forecast 2020 
and ESoWC 2020

# Aims 

1 Import OpenAQ dataset from many sources i.e. csv, ndjson or through api 

2 Import latest measurements for chosen OpenAQ stations

3 Import measurements for 6 months for choosen OpenAQ stations  

4 Import measurements for 18 months for choosen OpenAQ stations

5 Import measurements for every OpenAQ station and parameter

6 Import measurements for Stations, Cities, Country or Choosen Coordinate Centre and Radius

7 Get information about OpenAQ Dataset

# Implementation 

# 1 Importing from CSV, Ndjson and API 

## Milestone 1 Importing datasets from OpenAQ from csv 

"Milestone_1_Import_OpenAQ_applying_Datasetcsv.py"

## Importing from ndjson 

"Milestone_1_Import_OpenAQ_applying_Dataset_Wrangling.py"

## Importing datasets from pyAPI  

"Milestone1_Import_OpenAQ_Measurements_OpenAQStation.py"

## Import from OpenAQ API

"Milestone1_Import_OpenAQ_API_Download.py"

# 2 Import from choose stations 

Edit the Station in above

# 3 and 4 Time Schedule 

Change Begin and End Dates in above

# 5 Every OpenAQ Station 

Process for every station by name or region

# 6 Selected Dataset 

Change selection in above 

# 7 About the OpenAQ Dataset

## Getting Cities in Choosen Country

"Milestone1_Import_OpenAQ_Cities.py"

## Getting Station in Choosen Country 

"Milestone1_Import_OpenAQ_Countries.py"



# User Manual

## Importing from a csv 

Step 1 Download OpenAQ dataset from openAQ

Step 2 Convert to csv 

Step 3 Change csv requested in the script

in "Milestone_1_Import_OpenAQ_applying_Datasetcsv.py"

## Other implementations

In the python script


# Python Scripts 

1 Milestone1_Import_OpenAQ_Cities.py

Import cities that have openAQ locations for chosen country

2 Milestone1_Import_OpenAQ_Countries.py

Import countries that have openAQ locations

3 Milestone_1_Import_OpenAQ_applying_Dataset_Wrangling.py

Import OpenAQ Dataset from ndjson 

4 Milestone1_Import_OpenAQ_Measurements_Country.py

Import OpenAQ Measurement from a chosen country 

5 Milestone1_Import_OpenAQ_Measurements_OpenAQStation.py 

Import OpenAQ Measurements from chosen Station

6 Milestone_1_Import_OpenAQ_applying_Datasetcsv.py

Import OpenAQ dataset from a csv that has been downloaded from openAQ

7 Milestone1_Import_OpenAQ_API_Download.py

Queries the openAQ api for every stations measurements

It sometimes timesout while doing the query and should be done a few times to retry


Parameters: 

1 Milestone1_Import_OpenAQ_Cities.py

Chosen country


# Dependencies

Numpy 

Pandas 

openAQ
