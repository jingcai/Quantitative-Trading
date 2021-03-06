import os
import quandl
import logging
import pandas as pd


class Xignite:

    __slots__ = ['equitiesUrl1', 'equitiesUrl2', 'equitiesUrl3', 'equitiesUrl4', 'equitiesUrl5', 'equitiesUrl6']

    def __init__(self):
        self.equitiesUrl1 = 'http://www.xignite.com/xGlobalHistorical.csv/GetGlobalHistoricalQuotesRange?' + \
                            'IdentifierType='
        self.equitiesUrl2 = '&Identifier='
        self.equitiesUrl3 = '&AdjustmentMethod='
        self.equitiesUrl4 = '&StartDate='
        self.equitiesUrl5 = '&EndDate='
        self.equitiesUrl6 = '&_token=C53C982400FE4C43B1360C36980917E9'

    def download_adj_equity(self, tickers, start='', end='', identifier='Symbol'):
        """
        Extracts adjusted equity prices from xignite database
        :param tickers: List of equity tickers from xignite
        :param start: Default empty string takes first available data. Else mm/dd/yyyy string format required.
        :param end: Default empty string takes last available data. Else mm/dd/yyyy string format required.
        :param identifier: Supports 'Symbol', 'CUSIP'
        :return: DataFrame of prices
        """

        combined = []
        for ticker in tickers:
            logging.debug('Getting adjusted data for', ticker)
            if ' ' in ticker:
                adj_ticker = str.replace(ticker, ' ', '%20')
            else:
                adj_ticker = ticker
            url = self.equitiesUrl1 + identifier + self.equitiesUrl2 + adj_ticker + self.equitiesUrl3 + \
                  'SplitAndProportionalCashDividend' + self.equitiesUrl4 + start + self.equitiesUrl5 + \
                  end + self.equitiesUrl6
            df = pd.read_csv(filepath_or_buffer=url, index_col=26, parse_dates=[26])
            df = df['GlobalQuotes Last'].to_frame('Adj Close').sort_index(ascending=True)
            combined.append(df)

        if combined:
            data = pd.concat(combined, axis=1, join='outer')
            data = data.resample(rule='B').last()
            data = data.ffill()
            return data

    def download_non_adj_equity(self, tickers, start='', end='', identifier='Symbol'):
        """
        Extracts non-adjusted equity prices from xignite database
        :param tickers: List of equity tickers from xignite
        :param start: Default empty string takes first available data. Else mm/dd/yyyy string format required.
        :param end: Default empty string takes last available data. Else mm/dd/yyyy string format required.
        :param identifier: Supports 'Symbol', 'CUSIP'
        :return: DataFrame of prices
        """

        combined = []
        for ticker in tickers:
            logging.debug('Getting non adjusted data for', ticker)
            if ' ' in ticker:
                adj_ticker = str.replace(ticker, ' ', '%20')
            else:
                adj_ticker = ticker
            url = self.equitiesUrl1 + identifier + self.equitiesUrl2 + adj_ticker + self.equitiesUrl3 + \
                  'None' + self.equitiesUrl4 + start + self.equitiesUrl5 + \
                  end + self.equitiesUrl6
            df = pd.read_csv(filepath_or_buffer=url, index_col=26, parse_dates=[26])
            df = df[['GlobalQuotes Last',
                     'GlobalQuotes SplitRatio',
                     'GlobalQuotes CummulativeCashDividend',
                     'GlobalQuotes CummulativeStockDividendRatio']].sort_index(ascending=True)
            df.columns = ['Close', 'SplitRatio', 'CumCashDividend', 'CumStkDividend']
            combined.append(df)

        if combined:
            data = pd.concat(combined, axis=1, join='outer')
            data = data.resample(rule='B').last()
            data = data.ffill()
            return data


if __name__ == '__main__':
    path = r'C:\Users\JD\Google Drive\Quantitative Trading\Data'
    logging.basicConfig(level=logging.DEBUG)
    tickers = ['WEED.XTSE', 'ACB.XTSE', 'APH.XTSE', 'FIRE.XTSE']
    downloader = Xignite()
    for ticker in tickers:
        logging.debug('Downloading', ticker, '...')
        adj = downloader.download_adj_equity(tickers=[ticker])
        nonadj = downloader.download_non_adj_equity(tickers=[ticker])
        prices = pd.concat([adj, nonadj], axis=1, join='inner')
        prices.to_csv(os.path.join(path, ticker + '.csv'))
