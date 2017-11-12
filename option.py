import os
import time
import sqlite3
import logging
import datetime
import numpy as np
import pandas as pd


class Option:

    __slots__ = ['db', 'origin_path', 'conn_path', 'conn', 'cursor']

    def __init__(self):
        self.db = 'options.db'
        self.origin_path = r'C:\Users\JD\Google Drive\trading\data'
        self.conn_path = os.path.join(self.origin_path, self.db)
        self.conn = sqlite3.connect(self.conn_path)
        self.cursor = self.conn.cursor()

    def create_db(self, names):
        for name in names:
            self.cursor.execute(
                '''CREATE TABLE ? 
                (date underlying_symbol underlying_price option_root option_type 
                expiration strike last bid ask volume open_int t1_optn_int)''',
                name)

            for yr in ['2012', '2013', '2014', '2015', '2016', '2017']:
                for mth in ['JAN', 'FEB', 'MAR', 'APR', 'MAY', 'JUN', 'JUL', 'AUG', 'SEP', 'OCT', 'NOV', 'DEC']:
                    for dataset in os.listdir('/'.join([self.origin_path, yr, mth])):
                        logging.debug('Importing', dataset, '...')
                        df = pd.read_csv(dataset, header=0, parse_dates=[6, 7], dayfirst=False)
                        relevant = df.ix[df['UnderlyingSymbol'] == name, :]
                        lst_of_tuples = [tuple(row.values) for row in relevant.iterrows()]
                        sql_insertion_code = 'INSERT INTO ' + name + ' VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)'
                        self.cursor.executemany(sql_insertion_code, lst_of_tuples)

            self.conn.commit()

    def close_db(self):
        self.conn.close()




    """
    def __init__(self, underlying, transaction, opt_type, strike_chg, freq):
        self.underlying = underlying
        self.transaction = transaction
        self.opt_type = opt_type
        self.strike_chg = strike_chg
        self.freq = freq
        self.columns = ['Date', 'Spot', 'Expiry', 'Strike', 'Initial', 'Last', 'Rollover', 'MTM']
        self.dates, self.spots, self.expiries, self.strikes, self.initials, self.lasts, self.rollovers, self.mtm = \
            [], [], [], [], [], [], [], []
        self.roll_profit = 0

    def _nearest(self, col_name, pivot):
        if col_name == 'Expiration':
            vals = self.data.drop_duplicates(subset=col_name, keep='first', inplace=False)  # Get all possible expiry dates in option dataset
        else:

            # For different expirations, strikes may differ due to new release by exchange based on spot.
            # Thus important to filter by expirations. Merely dropping duplicates from original dataset might
            # lead to strike in other expirations being chosen but not available in desired expiration
            self.relevant_strikes = self.data.ix[self.data['Expiration'] == self.expiries[-1]]
            vals = self.relevant_strikes.drop_duplicates(subset=col_name, keep='first', inplace=False)

        vals = vals[col_name]
        best = min(vals, key=lambda val: abs(val - pivot))
        print('Rolling', self.transaction, self.opt_type, 'for', self.underlying, 'on', col_name, 'of', best,
              'at spot =', self.spots[-1], '...')
        return best

    def _update_rollover(self):
        if not self.expiries:
            self.rollovers.append(False)
        else:
            self.rollovers.append(self.dates[-1] >= self.expiries[-1])

    def _update_expiry(self):
        if self.rollovers[-1]:
            self.expiries.append(Option._nearest(self, 'Expiration', self.dates[-1] + self.freq))  # Rollover so have to choose new expiration based on duration of option period desired
        else:
            if self.expiries:
                self.expiries.append(self.expiries[-1])  # Use expiry from previous's day backtest
            else:
                self.expiries.append(Option._nearest(self, 'Expiration', self.dates[-1] + self.freq))  # First day of backtest so have to choose new expiration based on duration of option period desired

    def _update_strike(self):
        if self.rollovers[-1]:
            self.strikes.append(Option._nearest(self, 'Strike', self.spots[-1] * self.strike_chg))  # Rollover so have to choose strike based on spot
        else:
            if self.strikes:
                self.strikes.append(self.strikes[-1])  # Use strike from previous's day backtest
            else:
                self.strikes.append(Option._nearest(self, 'Strike', self.spots[-1] * self.strike_chg))  # First day of backtest so have to choose strike based on spot

    def _update_last(self):
        self.relevant_strikes = self.data.ix[self.data['Expiration'] == self.expiries[-1]]
        last = self.relevant_strikes.ix[self.relevant_strikes['Strike'] == self.strikes[-1], 'Last']
        self.lasts.append(last.values[0])

    def _update_initial(self):
        if self.rollovers[-1]:
            self.initials.append(self.lasts[-1])
        else:
            if self.initials:
                self.initials.append(self.initials[-1])
            else:
                self.initials.append(self.lasts[-1])

    def _update_profits(self):
        if self.rollovers[-1]:
            self.roll_profit = self.mtm[-1]
            self.mtm.append(self.mtm[-1])
        else:
            if self.transaction == 'long':
                self.mtm.append(self.roll_profit + self.lasts[-1] - self.initials[-1])
            else:
                self.mtm.append(self.roll_profit + self.initials[-1] - self.lasts[-1])

    def backtest(self, data):
        self.data = data[data['Type'] == self.opt_type]
        self.data.index = range(len(self.data))

        self.dates.append(self.data.ix[0, 'DataDate'])
        self.spots.append(self.data.ix[0, 'UnderlyingPrice'])

        Option._update_rollover(self)
        Option._update_expiry(self)
        Option._update_strike(self)
        Option._update_last(self)
        Option._update_initial(self)
        Option._update_profits(self)

    def finish(self):
        self.results = pd.DataFrame(index=range(len(self.lasts)), columns=self.columns)
        self.results['Date'] = self.dates
        self.results['Spot'] = self.spots
        self.results['Expiry'] = self.expiries
        self.results['Strike'] = self.strikes
        self.results['Initial'] = self.initials
        self.results['Last'] = self.lasts
        self.results['MTM'] = self.mtm
        self.results['Rollover'] = self.rollovers
    """
