# Import packages
import os
import sys
import logging
import logging.config
import pandas as pd
import numpy as np
import datetime as dt
from azure.datalake.store import core, lib
from sklearn.model_selection import train_test_split
from sklearn import metrics

# Custom imports
import prepare_data as prepdat
import settings as s
import credentials as c
#import ridge_regression as rr

def main():
    #Create logger
    log_format = '%(asctime)s - %(name)s - %(levelname)s - %(funcName)s - %(message)s'
    logging.basicConfig(format=log_format, level=logging.INFO, stream=sys.stdout)



    if s.from_database:
        # Get raw data from database
        raw_data = prepdat.get_data()
        prepdat.write_data_to_pickle(raw_data, s.path_data_folder + 'data_prepared.pkl')
    else:
        # Retrieve data from pickle
        raw_data = prepdat.get_data_from_pickle(s.path_data_folder + 'data_prepared.pkl')



    data_pricing = prepdat.get_pricing_data(raw_data, s.path_input_folder)
    data_prices = prepdat.get_prices(data_pricing, s.path_input_folder)

    columns_drop = ['BKR_BOOKING','DEPARTURE_AIRPORT', 'ARRIVAL_AIRPORT']
    data = prepdat.delete_columns(data_prices, columns_drop)



    print(data.head())
    print(data.columns)

    X = data[:-1]
    y = data[-1:]

    #train_X, test_X, train_y, test_y = train_test_split(X, y, test_size=0.2, random_state=500)







if __name__ == '__main__':
    main()