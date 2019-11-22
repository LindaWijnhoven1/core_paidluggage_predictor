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
import configure_log as l
from models.baseline import baseline as bl
from models.ridge_regression import ridge_regression as rr
from models.ridge_regression import ridge_cv as rr2
from models.random_forest_regression import random_forest_regression as rfr
from models.neural_network import neural_network as nn
from evaluation_metric import get_rmse, get_r2, rmse_second



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
                   #'SOURCE',
                   'WEEKDAY_OF_DEPARTURE',
                   'MONTH_OF_DEPARTURE',
                   'TIMESLOT_OF_DEPARTURE',
                   'WEEKDAY_OF_BOOKING'
        #,
                   #'WEEKDAY_OF_BOOKING_BAG'
                     ]
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
                    'LEVEL',
                    'BOOKING_BAG_DBD'
                    ####DELETE DATA BASED ON CORRELATIONS
                    #'GROUPBOOKING'
                    #'DIRECTION',
                    #'SEASONALITY'
                    ]
    data = prepdat.delete_columns(data_dummies, columns_drop)

    ###DELETE IF DATA IS RETRIEVED AGAIN
    data['GROUPBOOKING'] = pd.to_numeric(data['GROUPBOOKING'])
    data['SEASONALITY'] = pd.to_numeric(data['SEASONALITY'])

    """"Retrieve heatmap correlation"""
    #corr_matrix = data.corr()
    #print(corr_matrix)
    #corr_matrix.to_csv("corr_matrix.csv")
    #print(data['GROUPBOOKING'].corr(data['WEIGHT_OF_ITEMS']))
    #print(data['SEASONALITY'].corr(data['WEIGHT_OF_ITEMS']))
    """End of heatmap correlation"""




    logger.info('Used features: ' + data.columns)

    logger.info('Retrieve target and features - started')
    X = data.drop(['WEIGHT_OF_ITEMS'], axis=1).fillna(0)
    y = data['WEIGHT_OF_ITEMS'].fillna(0)

    logger.info('Standardize continuous features - started')
    columns_std_x = ['TOTAL_LEG_DISTANCE_KM',
                   'BOOKING_DBD',
                   #'BOOKING_BAG_DBD',
                   'LENGTH_OF_STAY',
                   'NBR_OF_PAX_IN_PNR',
                   'BOOKING_TICKET_REVENUE_INCL_TAX',
                   'PRICE_15KG',
                   'PRICE_20KG',
                   'PRICE_25KG',
                   'PRICE_30KG',
                   'PRICE_40KG',
                   'PRICE_50KG'
                     ]

    ct = ColumnTransformer([
        ('Standardized', StandardScaler(), columns_std_x)
    ], remainder='passthrough')

    ct.fit_transform(X[columns_std_x])

    logger.info('Target to Numpy - started')
    y = y.to_numpy().reshape(-1, 1)

    logger.info('Split test set - started')
    train_X, test_X, train_y, test_y = train_test_split(X, y, test_size=0.2, random_state=500)

    if s.run_baseline:
        logger.info('Set baseline - started')
        y_mean_train = np.repeat(train_y.mean(), len(train_y))
        baseline_train = bl(train_y, y_mean_train)

        y_mean_test = np.repeat(test_y.mean(), len(test_y))
        baseline_test = bl(test_y, y_mean_test)

        print(baseline_train)
        logger.info('Baseline result training: ' + str(baseline_train))
        print(baseline_test)
        logger.info('Baseline result test: ' + str(baseline_test))

    if s.run_ridge:
        logger.info('Start training ridge regression - started')
        _, params, train_rmse, model_rr, grid_result = rr(train_X, train_y)
        test_r2 = get_r2(test_y, grid_result.predict(test_X))
        test_rmse = get_rmse(test_y, grid_result.predict(test_X))

        print('train params: ', params)
        print("train rmse: ", train_rmse)
        print("test_r2: ", test_r2)
        print("test_rmse: ", test_rmse)
        logger.info('Ridge regression parameters: ' + str(params))
        logger.info('Ridge regression result training: ' + str(train_rmse))
        logger.info('Ridge regression result test r2: ' + str(test_r2))
        logger.info('Ridge regression result test rmse: ' + str(test_rmse))

    if s.run_forest:
        logger.info('Start training random forest regression - started')
        _, params, train_rmse, model_rfr, grid_result = rfr(train_X, train_y)
        test_r2 = get_r2(test_y, grid_result.predict(test_X))
        test_rmse = get_rmse(test_y, grid_result.predict(test_X))

        print('train params: ', params)
        print("train rmse: ", train_rmse)
        print("test_r2: ", test_r2)
        print("test_rmse: ", test_rmse)
        logger.info('Random forest regression parameters: ' + str(params))
        logger.info('Random forest regression result training: ' + str(train_rmse))
        logger.info('Random forest regression result test r2: ' + str(test_r2))
        logger.info('Random forest regression result test rmse: ' + str(test_rmse))

    if s.run_neural:
        logger.info('Start neural network - started')
        _, params, train_rmse, optimizer, grid_result = nn(train_X, train_y)
        test_r2 = get_r2(test_y, grid_result.predict(test_X))
        test_rmse = get_rmse(test_y, grid_result.predict(test_X))

        print('train params: ', params)
        print("train rmse: ", train_rmse)
        print("test_r2: ", test_r2)
        print("test_rmse: ", test_rmse)
        logger.info('Neural network parameters: ' + str(params))
        logger.info('Neural network optimizer: ' + str(optimizer))
        logger.info('Neural network result training: ' + str(train_rmse))
        logger.info('Neural network result test r2: ' + str(test_r2))
        logger.info('Neural network result test rmse: ' + str(test_rmse))



if __name__ == '__main__':
    main()