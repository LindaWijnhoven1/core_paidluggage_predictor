from matplotlib import pyplot as plt
import numpy as np
from sklearn.linear_model import Ridge
from sklearn.model_selection import GridSearchCV
from sklearn.metrics import make_scorer
from sklearn.metrics import mean_squared_error, r2_score
from math import sqrt

from evaluation_metric import get_rmse, get_r2

def ridge_regression(train_x, train_y):
    parameters = {'alpha': [5,6,7,8,9,10,11,12]}
    #cv = {'cv': [3,5]}
    #scorer = make_scorer(rmse_r2, greater_is_better = False)
    scoring = {'r2': make_scorer(get_r2),
               'rmse': make_scorer(get_rmse, greater_is_better=False)}

    clf = Ridge()
    rr = GridSearchCV(clf, parameters, scoring=scoring, cv=3, refit='rmse')
    grid_result = rr.fit(train_x, train_y)

    scores = grid_result.cv_results_
    best_params = grid_result.best_params_
    best_score = grid_result.best_score_

    return scores, best_params, best_score




