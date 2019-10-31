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
from datetime import datetime

# Custom imports
import prepare_data as prepdat
import settings as s
import credentials as c
#import ridge_regression as rr
import configure_log as l

def main():
    # Create logger
    log_path = s.path_log_folder
    log_name = s.filename_log
    logger = l.configure_logger(__name__, log_path + log_name)
    logging.getLogger().handlers[1].doRollover()

    logger.info('Run  - started ' + str(datetime.now()))

    if s.from_database:
        logger.info('Data retrieval from DWH - started')
        # Get raw data from database
        raw_data = prepdat.get_data()
        prepdat.write_data_to_pickle(raw_data, s.path_data_folder + 'data_prepared.pkl')
        logger.info('Data retrieval from DWH - finished')
    else:
        logger.info('Data retrieval from pickle - started')
        # Retrieve data from pickle
        raw_data = prepdat.get_data_from_pickle(s.path_data_folder + 'data_prepared.pkl')
        logger.info('Data retrieval from pickle - finished')

    logger.info('Import pricing levels - started')
    data_pricing = prepdat.get_pricing_data(raw_data, s.path_input_folder)

    logger.info('Import prices - started')
    data_prices = prepdat.get_prices(data_pricing, s.path_input_folder)

    logger.info('Retrieve final dataset - started')
    columns_drop = ['BKR_BOOKING','DEPARTURE_AIRPORT', 'ARRIVAL_AIRPORT']
    data = prepdat.delete_columns(data_prices, columns_drop)





    print(data.head())
    print(data.columns)

    X = data[:-1]
    y = data[-1:]

    #train_X, test_X, train_y, test_y = train_test_split(X, y, test_size=0.2, random_state=500)







if __name__ == '__main__':
    main()