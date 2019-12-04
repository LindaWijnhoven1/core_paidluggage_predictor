# core_paidluggage_predictor

**Description**
This is a thesis project in collaboration with Transavia (Revenue Management). The code tests the performance of three regression models (RMSE score) on how it is able to predict the total mass of paid luggage added to a booking. 

**Installation**
This project contains a Venv to set up the environment. 
In order to run this project, it is necessary to clone it locally and set up the environment (requirements.txt). Use command $ `pipenv install` to install environment from requirements.txt.
Within PyCharm, set the Project Interpreter (File-> Settings -> Project:<project_name> -> Project Interpreter) to the right VirtualEnv. Click on the settings-wheel -> Add. Now select the virtualenv that is shows in existing or new environment.

This project is supported for **python 3** only.

**Data Sources**
In this project two folders should be created:
* Data
* Input

The data folder contains the raw pickle of data after the DWH has been run and can be used for quick operations. 
The input file contains two files and are needed to merge the data on available prices:
* Prices
* Pricing

The pricing file shows the levels of prices at a specific moment in time in the past. The prices show the available prices of all paid luggage kilograms.

**Credentials**
The credentials_examply.py provides insight on which credentials are needed. 
DWH can be accessed by production credentials from the RM team or with the use of personal credentials. 

**Authors**
Linda Wijnhoven 


