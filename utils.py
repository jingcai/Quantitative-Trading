import os
import math
import numpy as np
import pandas as pd
from statsmodels.tsa.stattools import adfuller
from statsmodels.tools.tools import add_constant
from statsmodels.regression.linear_model import OLS


def stkDvdAdjustment(price, stkDvd):
    return price / stkDvd


def cashDvdAdjustment(price, cashDvd):
    return price - cashDvd


def stkSplitAdjustment(price, splitRatio):
    return price / splitRatio


def chkDataExists(path, file):
    return file in os.listdir(path)


def splitData(dataset, testRatio):
    idxToCutOff = math.ceil(testRatio * len(dataset))
    trainset = dataset.iloc[:-idxToCutOff, :]
    testset = dataset.iloc[-idxToCutOff:, :]
    return trainset, testset


def aggregate(dfs):
    if len(dfs) < 2:
        raise ValueError('Minimum of 2 dataframes required.')
    else:
        combined = pd.concat(dfs, axis=1, join='outer')
        combined = combined.resample(rule='B').last()
        combined.ffill(inplace=True)
        return combined


def computeLogRet(data):
    return np.log(data[1:] / data[:-1])


def computeSimpleRet(data):
    return data[1:] / data[:-1] - 1


def fitLinReg(x, y, addBias=True):
    if addBias:
        model = OLS(y, add_constant(x)).fit()
    else:
        model = OLS(y, x).fit()
    return model


def adfTest(vals):
    adfResult = adfuller(vals, autolag='AIC', regression='c')
    print('ADF Statistic:', adfResult[0])
    print('P-Value:', adfResult[1])
    print('Used Lags:', adfResult[2])
    print('Critical Value (10%):', adfResult[4]['10%'])
    print('Critical Value (5%):', adfResult[4]['5%'])
    print('Critical Value (1%):', adfResult[4]['1%'])


def linRegWithAdf(x, y, addBias=True):
    model = fitLinReg(x, y, addBias)
    print(model.summary())
    adfTest(model.resid)
    return model


def fitLinRegSimpleRetsWithAdf(x, y, addBias=True):
    xRets = computeSimpleRet(x)
    yRets = computeSimpleRet(y)
    return linRegWithAdf(xRets, yRets, addBias)


def fitLinRegLogRetsWithAdf(x, y, addBias=True):
    xRets = computeLogRet(x)
    yRets = computeLogRet(y)
    return linRegWithAdf(xRets, yRets, addBias)


def RSI(vals, timeperiod):
    df = vals.to_frame('NAV')
    df['Rets'] = df['NAV'].diff(1)
    df['gains'] = df['Rets'] * (df['Rets'] > 0)
    df['loss'] = df['Rets'] * (df['Rets'] < 0)
    df['avgGain'] = df['gains'].rolling(window=timeperiod).mean()
    df['avgLoss'] = df['loss'].abs().rolling(window=timeperiod).mean()
    df['rs'] = df['avgGain'] / df['avgLoss']
    df['rsi'] = 100 - 100 / (1 + df['rs'])
    return df['rsi'].values


def BBANDS(vals, timeperiod, upperMultiplier, lowerMultiplier):
    df = vals.to_frame('NAV')
    df['SMA'] = df['NAV'].rolling(window=timeperiod).mean()
    df['Std'] = df['NAV'].rolling(window=timeperiod).std()
    df['Upper Bollinger'] = df['SMA'] + df['Std'] * upperMultiplier
    df['Lower Bollinger'] = df['SMA'] - df['Std'] * lowerMultiplier
    return df['Upper Bollinger'].values, df['SMA'].values, df['Lower Bollinger'].values


"""
MA Model
strategy['a(t)'] = 0
for i in range(1, len(strategy)):
    strategy.loc[strategy.index[i], 'a(t)'] = strategy.loc[strategy.index[i], 'r(t)'] + armaModel.params[0] * strategy.loc[strategy.index[i-1], 'a(t)']
strategy.head()
"""