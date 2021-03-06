from sklearn.base import clone
from sklearn.metrics import mean_squared_error, r2_score
from sklearn.model_selection import TimeSeriesSplit
from sklearn.preprocessing import StandardScaler
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np


def tscv_regression(x, y, n_cv_sets, model):

    # Preparing data structures for capturing results
    train_actual, test_actual = [], []
    train_preds, test_preds = [], []
    train_errors, test_errors = [], []
    train_r2_scores, test_r2_scores = [], []

    # Preparing datasets for time series split
    x_copy, y_copy = np.copy(x), np.copy(y)
    tscv = TimeSeriesSplit(n_splits=n_cv_sets)

    # Running cross validation
    for train_idx, test_idx in tscv.split(x_copy):
        train_x, train_y = x_copy[train_idx], y[train_idx]
        test_x, test_y = x_copy[test_idx], y[test_idx]

        # Scaling the X data
        scaler = StandardScaler()
        scaled_train_x = scaler.fit_transform(train_x)
        scaled_test_x = scaler.transform(test_x)

        # Fitting the model
        model = clone(model)
        model.fit(scaled_train_x, train_y)

        # Predicting with model
        train_pred, test_pred = model.predict(scaled_train_x), model.predict(scaled_test_x)
        train_actual.append(train_y); test_actual.append(test_y)
        train_preds.append(train_pred); test_preds.append(test_pred)
        train_errors.append(np.sqrt(mean_squared_error(train_y, train_pred)))
        test_errors.append(np.sqrt(mean_squared_error(test_y, test_pred)))
        train_r2_scores.append(r2_score(train_y, train_pred))
        test_r2_scores.append(r2_score(test_y, test_pred))

    return train_actual, train_preds, test_actual, test_preds, \
           train_errors, test_errors, train_r2_scores, test_r2_scores


def plot_rmse(train_errors, test_errors):
    print('Mean train_error:', np.mean(train_errors), 'Std train_error:', np.std(train_errors))
    print('Mean test_error:', np.mean(test_errors), 'Std test_error:', np.std(test_errors))
    plt.plot(train_errors, label='train_error')
    plt.plot(test_errors, label='test_error')
    plt.legend()
