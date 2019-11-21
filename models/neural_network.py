from evaluation_metric import get_rmse, get_r2
from sklearn.metrics import make_scorer

from keras.models import Sequential
from keras.layers import Dense
from keras.layers import Dropout
from keras.callbacks import EarlyStopping
from keras.optimizers import Adam
from keras.wrappers.scikit_learn import KerasRegressor

from sklearn.model_selection import GridSearchCV

def neural_network(train_x, train_y):
    parameters = {'epochs': [15, 10],
                  'batch_size': [100, 150,200]
                  }

    #optimizer = Adam(lr=0.001, beta_1=0.9, beta_2=0.999)
    optimizer = 'rmsprop'

    es = EarlyStopping(monitor='loss', mode='min', verbose=2, min_delta=0.5, patience=1)

    scoring = {'r2': make_scorer(get_r2),
               'rmse': make_scorer(get_rmse, greater_is_better=False)}


    def create_network():
        rgr = Sequential()
        rgr.add(Dense(units=256, activation='relu', input_dim=train_x.shape[1]))
        rgr.add(Dense(units=128, activation='relu'))
        rgr.add(Dense(units=64, activation='relu'))
        rgr.add(Dense(units=1))

        rgr.compile(loss='mean_squared_error',
                    optimizer=optimizer)
        return rgr

    grid_rgr = KerasRegressor(build_fn=create_network, verbose=2, )

    nn = GridSearchCV(grid_rgr, parameters, scoring='neg_mean_squared_error', cv=3) #refit='rmse')
    grid_result = nn.fit(train_x, train_y, callbacks=[es])

    scores = grid_result.cv_results_
    best_params = grid_result.best_params_
    best_score = grid_result.best_score_

    return scores, best_params, best_score, optimizer, grid_result


def neural_network1(train_x, train_y):
    scoring = {'r2': make_scorer(get_r2),
               'rmse': make_scorer(get_rmse, greater_is_better=False)}

    optimizer = Adam(lr=0.001, beta_1=0.9, beta_2=0.999)

    rgr = Sequential()
    rgr.add(Dense(units=256, activation='relu', input_dim=train_x.shape[1]))
    rgr.add(Dense(units=128, activation='relu'))
    rgr.add(Dense(units=64, activation='relu'))
    rgr.add(Dense(units=1))

    rgr.compile(loss='mean_squared_error',
                optimizer=optimizer
                )

    scores = rgr.fit(train_x, train_y, batch_size=5, epochs=10, verbose=2)

    scores_ = rgr.evaluate(train_x, train_y)

    return scores, scores_

