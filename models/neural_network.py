# Import packages
from sklearn.metrics import make_scorer
from keras.models import Sequential
from keras.layers import Dense
from keras.layers import Dropout
from keras.callbacks import EarlyStopping
from keras.optimizers import Adam
from keras.wrappers.scikit_learn import KerasRegressor
from sklearn.model_selection import GridSearchCV

# Custom imports
from evaluation_metric import get_rmse, get_r2

def neural_network(train_x, train_y):
    parameters = {'epochs': [10,15],
                  'batch_size': [150,200]
                  }

    optimizer = Adam(lr=0.001, beta_1=0.9, beta_2=0.999)
    #optimizer = 'rmsprop'

    es = EarlyStopping(monitor='loss', mode='min', verbose=2, min_delta=0.5, patience=1)

    scoring = {'r2': make_scorer(get_r2),
               'rmse': make_scorer(get_rmse, greater_is_better=False)}


    def create_network():
        rgr = Sequential()
        rgr.add(Dense(units=500, activation='relu', input_dim=train_x.shape[1]))
        rgr.add(Dropout(0.1))
        rgr.add(Dense(units=300, activation='relu'))
        rgr.add(Dense(units=200, activation='relu'))
        rgr.add(Dense(units=100, activation='relu'))
        rgr.add(Dense(units=50, activation='relu'))
        rgr.add(Dense(units=1))

        rgr.compile(loss='mean_squared_error',
                    optimizer=optimizer)
        return rgr

    grid_rgr = KerasRegressor(build_fn=create_network, verbose=2)

    nn = GridSearchCV(grid_rgr, parameters, scoring='neg_mean_squared_error', cv=3)
    grid_result = nn.fit(train_x, train_y, callbacks=[es])

    scores = grid_result.cv_results_
    best_params = grid_result.best_params_
    best_score = grid_result.best_score_

    return scores, best_params, best_score, optimizer, grid_result
