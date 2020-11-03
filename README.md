  
Air Quality Observations Quality Control  

Description
Validating and removing errors outliers from surface air quality observations from individual sensors so that these observation can be compared to ECMWF's CAMS air quality forecasts. By clustering analysis on these observations more reliable observations can be identified. Enhancing these observations by attaching data about factors that affect air quality these observations can have more credibility about their accuracy. CAMS lacks credible surface air quality observations in many parts of the world, often in the most polluted area such as in India or Africa. Some observations are available for these areas from data harvesting efforts such as openAQ but there is no quality control applied to the data, and it is often not well known if the observations are made in a rural, urban or heavily polluted local environment. This information on the environment is important because the very locally influenced measurements are mostly not representative for the horizontal scale (40 km) of the CAMS forecasts and should therefore not be used for the evaluation of the CAMS model.

Completed for ECMWF European Centre for Medium Weather Forecast 2020 
and ESoWC 2020

Implementation 

Milestone 3 Classification of AQ Stations 

Aims 
1 Choose an upper bound of values and identify value over to be outliers
2 Choose a lower bound of values 
3 Choose an increment on measurements that is acceptable for both increasing and decreasing values 
4 Find How many stations don’t measure every 15 minutes through a day and when are these are
5 Find stagnant measurements that don't change over a chosen amount 

User Manual

UserManual_Milestone_3_Pecos_Quality_Control_Classification_of_Stations.pdf
(This is for Milestone3_Pecos_Importing_OpenAQ_API_Dataset_Classification_of_Measurements.py)


Parameters 
1 Higher bound
2 Lower Bound 
3 Timestep of expected measurements
4 The higher bound and lower bound that designate stagnant measurements  
5 Increment over measurements 

Presentation results

The scripts utput to test_results.csv and monitoring_report.html
(There are examples of these in the github)

Python Scripts 

1 Milestone3_Pecos_6Month_Importing_OpenAQ_API_Dataset_Classification_of_Measurements_6Months.py
2 Milestone3_Pecos_Importing_OpenAQ_API_Dataset_Classification_of_Measurements.py

2 Milestone3_Pecos_Importing_OpenAQ_API_Dataset_Classification_of_Measurements.py

A Script for importing OpenAQ dataset for One country and one parameter 

1 Milestone3_Pecos_6Month_Importing_OpenAQ_API_Dataset_Classification_of_Measurements_6Months.py

A Script to get 6 Months of OpenAQ dataset from one station and one parameter. The defaults are parameter pm25 and station US Diplomatic Post: Hyderabad 

Parameters: 

OpenAQ Location: Line 33

"res_1 = api.measurements(location='US Diplomatic Post: Hyderabad', parameter='pm25', date_to=dt_end, date_from=dt_begin, limit=10000, df=True)
"

OpenAQ Parameter: Line 33
                                                                                 
"res_1 = api.measurements(location='US Diplomatic Post: Hyderabad', parameter='pm25', date_to=dt_end, date_from=dt_begin, limit=10000, df=True)"

OpenAQ Date Range: Line 21 and 22

"dt_begin = date(2020,3,1)
dt_end = date(2020,9,1)"

1 Higher bound: Step 6 Line 87

"pm.check_range([0, 200], key='value')"

"pm.check_range([Lower Bound, High Bound], key='value')"

2 Lower Bound: Step 6 Line 87 

"pm.check_range([0, 200], key='value')"

"pm.check_range([Lower Bound, High Bound], key='value')"

3 Timestep of expected measurements: Step 4 Line 65

"pm.check_timestamp(900)"

4 The higher bound and lower bound that designate stagnant measurements:  Step 7 Line 106  

"pm.check_delta([None, 10], window=3600, key='value')"

5 Increment over measurements: Step 8 Line 124

pm.check_increment([None, 20], key='value') 

 


Dependencies

Pecos Package 

https://pecos.readthedocs.io/en/stable/overview.html
https://github.com/sandialabs/pecos

