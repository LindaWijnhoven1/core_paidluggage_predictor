from sklearn import metrics
import numpy as np
from math import sqrt
from sklearn.metrics import mean_squared_error, r2_score

def get_rmse(y, y_pred):
    rmse = np.sqrt(mean_squared_error(y, y_pred))
    print
    'RMSE: %2.3f' % rmse
    return rmse


def get_r2(y, y_pred):
    r2 = r2_score(y, y_pred)
    print
    'R2: %2.3f' % r2
    return r2

#def rmse_r2(y_true, y_pred):
#    score = get_rmse(y_true, y_pred)
#    get_r2(y_true, y_pred)
#    return score