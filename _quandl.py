import os
import quandl
import logging


def download(tickers):
    for ticker in tickers:
        logging.debug('Downloading', ticker, '...')
        data = quandl.get(ticker)
        ticker = ticker.split('/')[1]
        data.to_csv(os.path.join(path, ticker + '.csv'))


if __name__ == '__main__':
    path = r'C:\Users\JD\Google Drive\Quantitative Trading\Data'
    tickers = ['WIKI/AAPL']
    download(tickers)
