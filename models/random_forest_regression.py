from evaluation_metric import get_rmse, get_r2
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import GridSearchCV
from sklearn.metrics import make_scorer


def random_forest_regression(train_x, train_y):
    parameters = {'max_depth': [10,15,20,21],
                  'n_estimators': [100, 200, 500]}
    scoring = {'r2': make_scorer(get_r2), 'rmse': make_scorer(get_rmse, greater_is_better=False)}

    clf = RandomForestRegressor()
    #max_depth=best_params["max_depth"], n_estimators=best_params["n_estimators"],
                                #random_state=False, verbose=False)
    rfr = GridSearchCV(clf, parameters, scoring=scoring, cv=3, refit='rmse')
    grid_result = rfr.fit(train_x, train_y)

    scores = grid_result.cv_results_
    best_params = grid_result.best_params_
    best_score = grid_result.best_score_

    return scores, best_params, best_score

