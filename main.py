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
from sklearn.preprocessing import OneHotEncoder, LabelEncoder
from sklearn.preprocessing import StandardScaler
from sklearn.compose import ColumnTransformer



# Import EDA packages
import seaborn as sns
import matplotlib
from matplotlib import pyplot as plt

# Custom imports
import prepare_data as prepdat
import settings as s
import credentials as c
#import ridge_regression as rr
import configure_log as l
from models.baseline import baseline as bl
from models.ridge_regression import ridge_regression as rr
from models.random_forest_regression import random_forest_regression as rfr
from models.neural_network import neural_network as nn


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
    data_prices = prepdat.get_prices(data_pricing, s.path_input_folder).fillna(0)

    logger.info('OneHotEncode categorical variables - started')
    columns_ohe = ['HUB_NL',
                   'COUNTRY_CODE',
                   'SOURCE',
                   'WEEKDAY_OF_DEPARTURE',
                   'MONTH_OF_DEPARTURE',
                   'TIMESLOT_OF_DEPARTURE',
                   'WEEKDAY_OF_BOOKING',
                   'WEEKDAY_OF_BOOKING_BAG']
    data_dummies = prepdat.dummy_columns(data_prices, columns_ohe)

    logger.info('Retrieve final dataset - started')
    columns_drop = ['DEPARTURE_DATE',
                    'HUB_NL',
                   'COUNTRY_CODE',
                   'SOURCE',
                   'WEEKDAY_OF_DEPARTURE',
                   'MONTH_OF_DEPARTURE',
                   'TIMESLOT_OF_DEPARTURE',
                   'WEEKDAY_OF_BOOKING',
                   'WEEKDAY_OF_BOOKING_BAG',
                   'BKR_BOOKING',
                   'DEPARTURE_AIRPORT',
                   'ARRIVAL_AIRPORT',
                   'BOOKING_DATE',
                   'BOOKING_DATE_BAG',
                   'PRICING_TIME',
                   'LEVEL']
    data = prepdat.delete_columns(data_dummies, columns_drop)

    print(len(data.columns))
    print(data.columns)

    logger.info('Retrieve target and features - started')
    X = data.drop(['WEIGHT_OF_ITEMS'], axis=1).fillna(0)
    y = data['WEIGHT_OF_ITEMS'].fillna(0)

    logger.info('Standardize continuous features - started')
    columns_std_x = ['TOTAL_LEG_DISTANCE_KM',
                   'BOOKING_DBD',
                   'BOOKING_BAG_DBD',
                   'LENGTH_OF_STAY',
                   'NBR_OF_PAX_IN_PNR',
                   'BOOKING_TICKET_REVENUE_INCL_TAX',
                   'PRICE_15KG',
                   'PRICE_20KG',
                   'PRICE_25KG',
                   'PRICE_30KG',
                   'PRICE_40KG',
                   'PRICE_50KG']

    ct = ColumnTransformer([
        ('Standardized', StandardScaler(), columns_std_x)
    ], remainder='passthrough')

    ct.fit_transform(X[columns_std_x])

    logger.info('Target to Numpy - started')
    y = y.to_numpy().reshape(-1, 1)

    print(X.shape)
    print(y.shape)

    logger.info('Split test set - started')
    train_X, test_X, train_y, test_y = train_test_split(X, y, test_size=0.2, random_state=500)



    if s.run_baseline:
        logger.info('Set baseline - started')
        y_mean = np.repeat(train_y.mean(), len(train_y))
        baseline = bl(train_y, y_mean)
        print(baseline)
        logger.info('Baseline results: ' + str(baseline))

    if s.run_ridge:
        logger.info('Start training ridge regression - started')
        ridge = rr(train_X, train_y)
        print(ridge)
        logger.info('Ridge regression results: ' + str(ridge))

    if s.run_forest:
        logger.info('Start training random forest regression - started')
        forest = rfr(train_X, train_y)
        print(forest)
        logger.info('Random forest regression results: ' + str(forest))

    if s.run_neural:
        logger.info('Start training neural network - started')
        neural = nn(train_X, train_y)
        print(neural)
        logger.info('Neural network results: ' + str(neural))






if __name__ == '__main__':
    main()