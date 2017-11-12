import os
import math
import logging
import numpy as np
import pandas as pd

PATH = r'C:\Users\JD\Google Drive\trading\data\historical equities data'


def aggregate_data(tickers, filter=None):
    if len(tickers) < 2:
        raise ValueError('Minimum of 2 tickers required.')
    else:
        try:
            dfs = [pd.read_csv(os.path.join(PATH, ticker + '.csv'), index_col=0, parse_dates=[0], dayfirst=True) for
                   ticker in tickers]
        except:
            raise ImportError('Not all data are available. Please check before trying again.')

        for ticker, df in zip(tickers, dfs):
            df.columns = [ticker + ' ' + col for col in df.columns]

        combined = pd.concat(dfs, axis=1, join='outer').resample(rule='B').last()
        combined.ffill(inplace=True)
        combined = combined.dropna()

        if not filter:
            return combined
        elif filter == 'close':
            logging.debug('Filtering out close prices only')
            return combined[[ticker + ' Close' for ticker in tickers]]
        elif filter == 'adj_close':
            logging.debug('Filtering out adjusted close prices only')
            return combined[[ticker + ' Adj Close' for ticker in tickers]]
        elif filter == 'log_ret':
            logging.debug('Filtering out log rets only')
            adj_close = combined[[ticker + ' Adj Close' for ticker in tickers]]
            log_rets = np.log(adj_close.pct_change(1) + 1)
            log_rets.columns = [ticker + ' Log Rets' for ticker in tickers]
            return log_rets.dropna()
        elif filter == 'simple_ret':
            logging.debug('Filtering out simple rets only')
            adj_close = combined[[ticker + ' Adj Close' for ticker in tickers]]
            simple_rets = adj_close.pct_change(1)
            simple_rets.columns = [ticker + ' Rets' for ticker in tickers]
            return simple_rets.dropna()
        else:
            raise ValueError(filter + ' is not a proper filter')


def split_data(data, testRatio):
    idx = math.ceil(testRatio * len(data))
    train = data.iloc[:-idx, :]
    test = data.iloc[-idx:, :]
    return train, test
