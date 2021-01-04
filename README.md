# air-quality-observation-classification
  
air-quality-observation-classification description 

Validating and removing errors outliers from surface air quality observations from individual sensors so that these observation can be compared to ECMWF's CAMS air quality forecasts. By clustering analysis on these observations more reliable observations can be identified. Enhancing these observations by attaching data about factors that affect air quality these observations can have more credibility about their accuracy. CAMS lacks credible surface air quality observations in many parts of the world, often in the most polluted area such as in India or Africa. Some observations are available for these areas from data harvesting efforts such as openAQ but there is no quality control applied to the data, and it is often not well known if the observations are made in a rural, urban or heavily polluted local environment. This information on the environment is important because the very locally influenced measurements are mostly not representative for the horizontal scale (40 km) of the CAMS forecasts and should therefore not be used for the evaluation of the CAMS model.

# Aims 

1 A Quality Control evaluation of openAQ dataset including Visual Analytics of OpenAQ Stations 

2 Find Outliers and Errors in OpenAQ Measurements 

3 Determine Reliability of OpenAQ Stations 

4 Allowing further analysis of openAQ dataset

# Implementation 

## Milestone1_Importing-datasets-from-OpenAQ

Importing OpenAQ datasets to dataframes

## Milestone2_Identifying_reliable_stations

Visual Analytics on OpenAQ datasets

## Milestone3_Pecos_Quality_Control

Pecos Quality Control evaluation on OpenAQ datasets to find Outliers and Errors

## Milestone4_Classification_of_Stations_attr

Nearest Highway to Station compared to statistics


# Dependencies

1 Pecos for Milestone 3

https://pecos.readthedocs.io/en/latest/installation.html

2 Gatherminer for Milestone 7 
An interactive visual tool for time series analysis.

Publication: Sarkar, Advait, Martin Spott, Alan F. Blackwell, and Mateja Jamnik. "Visual discovery and model-driven explanation of time series patterns." In Visual Languages and Human-Centric Computing (VL/HCC), 2016 IEEE Symposium on, pp. 78-86. IEEE, 2016.

http://dx.doi.org/10.1109/VLHCC.2016.7739668
Last updated April 2017, for v0.7

SPEED TIPS:

Under the gathering strategy, there is a new option 'Greedy imperfect seed' that is even faster and gives near-identical results.
For large datasets (e.g., around 3k or more rows) , unchecking "precompute distances" actually makes it faster because storing and retrieving from an n^2 distance matrix in memory becomes slower than just recomputing the distances on demand.
Gathering now works for quite large datasets (I think I have tried with up to 30k rows) You must uncheck "precompute distances". It can be very slow though (e.g., several minutes). If you keep the Chrome console open (View > Developer > Javascript console) then you can see whether gathering has crashed or is still running because I output status update messages from time to time.
Zooming on very large datasets will break, because Chrome has a maximum canvas size. It is very irritating that this bottleneck exists but I think it will require too much engineering to fix at this point.
FILE FORMATS: The file formats are very simple. The series data is a comma-separated file with each line containing one time series. There is no header line.

The series attributes is a comma-separated file with each line containing the attributes for the time series. There must be a header line containing the names of attributes. Therefore, the Nth line of the attributes file provides the attributes for the N-1th line of the series data file.

The CSV parsing, if I remember correctly, ignores any quote qualification. So if the actual values in your dataset contain commas, then you'll have to substitute them with some other character, otherwise the tool will break.
