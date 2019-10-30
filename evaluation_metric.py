from sklearn import metrics

def get_rmse(y, y_pred):
    return np.sqrt(metrics.mean_squared_error(y, y_pred))