# Data Engineering Challenge

## Overview

This project processes energy monitoring data from different sources (DG, Solar, and Battery) and calculates:

- Load data file and change Timestamp according to utc
- Hourly run hours for each source
- Average kW consumption/generation per hour

The data is processed using Python and Pandas.

---

## Project Structure

The Project is basically consists of 3 files 

- load_data.py
- task2_run_hours.py
- task3_power_kw.py

As a result, program generates 2 csv files 

- run_hours_output.csv
- power_kw.csv

## Assumption made

All three files are based according to their purposes. 

- load_data.py file will import data from the csv and checks that it is imported successfully
- Then, it will the Timestamp Series in Dataframe according to utc and updates the dataframe.
- task2_run_hours.py the updated dataframe will be imported from load_data.py file and firstly we breakdown the Timestamps to hour_window to perform our operation using datetime floor function into hour frame
- we will divide the dataframe into 3 parts using str.contains() DG, Solar and Battery into all three sources. So, we can perform functions on them eaily.
- then the dataframe will be grouped by site_code and hour_window and we apply sum method to get the count of DG in one hour
- We will apply and run_hours formula on that count to get the per hour run_hour for DG 
- Similarly, we do the same process for Solar, DG and battery 

- task3_power_kw.py we will perform all same function which we already performed in task 2 but with one modification when we groupby dataframe of DG we will take .agg() which means we perform 2 functions one is count and the other one is mean because we have to take the mean of the calculation which we made initially for power_kw.


