import os
import time
import sqlite3
import logging
import datetime
import numpy as np
import pandas as pd


class Db:

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


class Option:

    __slots__ = ['name', 'dates', 'ids', 'types', 'expiries', 'strikes', 'positions', 'underlying_prices', 'pnl']

    def __init__(self, name):
        self.name = name
        self.dates, self.ids, self.types, self.expiries, self.strikes, \
        self.positions, self.underlying_prices, self.pnl = \
            [], [], [], [], [], [], [], []

    def backtest(self, date, id, type, expiry, strike, position, underlying_price):
        self.dates.append(date)
        self.ids.append(id)
        self.types.append(type)
        self.expiries.append(expiry)
        self.strikes.append(strike)
        self.positions.append(position)
        self.underlying_prices.append(underlying_price)


def nearest(data, col_name, pivot):
    if col_name == 'Expiration':
        # Get all possible expiry dates in option dataset
        vals = data.drop_duplicates(subset=col_name, keep='first', inplace=False)
    else:
        # For different expirations, strikes may differ due to new release by exchange based on spot.
        # Thus important to filter by expirations. Merely dropping duplicates from original dataset might
        # lead to strike in other expirations being chosen but not available in desired expiration
        relevant_strikes = data.ix[data['Expiration'] == expiries[-1]]
        vals = relevant_strikes.drop_duplicates(subset=col_name, keep='first', inplace=False)

    vals = vals[col_name]
    best = min(vals, key=lambda val: abs(val - pivot))
    print('Rolling', self.transaction, self.opt_type, 'for', self.underlying, 'on', col_name, 'of', best, 'at spot =', self.spots[-1], '...')
    return best


def update_rollover(self):
    if not self.expiries:
        self.rollovers.append(False)
    else:
        self.rollovers.append(self.dates[-1] >= self.expiries[-1])


def update_expiry(self):
    if self.rollovers[-1]:
        self.expiries.append(nearest(self, 'Expiration', self.dates[-1] + self.freq))  # Rollover so have to choose new expiration based on duration of option period desired
    else:
        if self.expiries:
            self.expiries.append(self.expiries[-1])  # Use expiry from previous's day backtest
        else:
            self.expiries.append(nearest(self, 'Expiration', self.dates[-1] + self.freq))  # First day of backtest so have to choose new expiration based on duration of option period desired


def update_strike(self):
    if self.rollovers[-1]:
        self.strikes.append(nearest(self, 'Strike', self.spots[-1] * self.strike_chg))  # Rollover so have to choose strike based on spot
    else:
        if self.strikes:
            self.strikes.append(self.strikes[-1])  # Use strike from previous's day backtest
        else:
            self.strikes.append(nearest(self, 'Strike', self.spots[-1] * self.strike_chg))  # First day of backtest so have to choose strike based on spot


def update_last(self):
    self.relevant_strikes = self.data.ix[self.data['Expiration'] == self.expiries[-1]]
    last = self.relevant_strikes.ix[self.relevant_strikes['Strike'] == self.strikes[-1], 'Last']
    self.lasts.append(last.values[0])


def update_initial(self):
    if self.rollovers[-1]:
        self.initials.append(self.lasts[-1])
    else:
        if self.initials:
            self.initials.append(self.initials[-1])
        else:
            self.initials.append(self.lasts[-1])


def update_profits(self):
    if self.rollovers[-1]:
        self.roll_profit = self.mtm[-1]
        self.mtm.append(self.mtm[-1])
    else:
        if self.transaction == 'long':
            self.mtm.append(self.roll_profit + self.lasts[-1] - self.initials[-1])
        else:
            self.mtm.append(self.roll_profit + self.initials[-1] - self.lasts[-1])
