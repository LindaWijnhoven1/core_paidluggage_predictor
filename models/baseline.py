# Import packages
from evaluation_metric import get_rmse
from sklearn.metrics import mean_squared_error, r2_score

def baseline(y, y_mean):
    rmse = get_rmse(y, y_mean)
    r2 = r2_score(y, y_mean)

    return rmse, r2