from evaluation_metric import get_rmse

from keras.models import Sequential
from keras.layers import Dense
from keras.layers import Dropout
from keras.callbacks import EarlyStopping
from keras.optimizers import Adam
from keras.wrappers.scikit_learn import KerasRegressor

def neural_network(train_x, train_y):
    parameters = {'epochs': [5,10],
                  'batches': [5,10,100],
                  'optimizers': ['']}

    scoring = {'r2': make_scorer(get_r2),
               'rmse': make_scorer(get_rmse, greater_is_better=False)}


    def create_network(optimizer=Adam):
        clf = Sequential()
        clf.add(Dense(output_dim=128, activation='relu', input_dim=train_x.shape[1]))
        clf.add(Dense(output_dim=128, activation='relu'))
        clf.add(Dropout(0.1))
        clf.add(Dense(output_dim=128, activation='relu'))
        clf.add(Dense(output_dim=1, activation='sigmoid'))

        clf.compile(loss='mean_squared_error',
                        optimizer=optimizer,
                        metrics=scoring['rmse'])

        return clf

    clf = KerasRegressor(build_fn=create_network, verbose=0)

    nn = GridSearchCV(clf, parameters, scoring=scoring, cv=3, refit='rmse')
    grid_result = nn.fit(train_x, train_y)

    scores = grid_result.cv_results_
    best_params = grid_result.best_params_
    best_score = grid_result.best_score_

    return scores, best_params, best_scoreapt-get upgrade; apt autoremove
