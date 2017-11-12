import os
import quandl
import logging


path = r'C:\Users\JD\Google Drive\Quantitative Trading\Data'
tickers = ['WIKI/AAPL', 'WIKI/TSLA', 'WIKI/FB', 'WIKI/NFLX', 'WIKI/NVDA', 'WIKI/AMZN', 'WIKI/GOOGL',
           'WIKI/BAC', 'WIKI/C', 'WIKI/GS', 'WIKI/WFC', 'WIKI/MS']
for ticker in tickers:
    logging.debug('Downloading', ticker, '...')
    data = quandl.get(ticker)
    ticker = ticker.split('/')[1]
    data.to_csv(os.path.join(path, ticker + '.csv'))
