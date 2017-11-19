import os
import sqlite3
import logging
import pandas as pd


class Database:
    __slots__ = ['db', 'origin_path', 'conn_path', 'conn', 'cursor']

    def __init__(self):
        self.db = 'options.db'
        self.origin_path = r'C:\Users\JD\Google Drive\trading\data\historical us options data'
        self.conn_path = os.path.join(self.origin_path, self.db)
        self.conn = sqlite3.connect(self.conn_path)
        self.cursor = self.conn.cursor()

    def extract(self, name):
        sql_extraction = 'SELECT * from ' + name
        self.cursor.execute(sql_extraction)
        return self.cursor.fetchall()

    def create(self, names):
        for name in names:
            tbl_creation = 'CREATE TABLE IF NOT EXISTS ' + name + \
                           ' (date text, underlying_price real, option_root text, option_type text,' + \
                           'expiration text, strike real, last real, bid real, ask real, volume integer, ' + \
                           'open_int integer, t1_option_interest integer)'
            self.cursor.execute(tbl_creation)

        for yr in ['2012', '2013', '2014', '2015', '2016', '2017']:
            for mth in ['JAN', 'FEB', 'MAR', 'APR', 'MAY', 'JUN', 'JUL', 'AUG', 'SEP', 'OCT', 'NOV', 'DEC']:
                path = '/'.join([self.origin_path, yr, mth])
                for dataset in os.listdir(path):
                    logging.debug('Importing ' + dataset)
                    df = pd.read_csv(os.path.join(path, dataset), header=0)

                    for name in names:
                        relevant = df.ix[df['UnderlyingSymbol'] == name, :]
                        if relevant.empty:
                            logging.debug('There is no options for ' + name + ' in' + dataset)
                        else:
                            relevant = relevant[['DataDate', 'UnderlyingPrice', 'OptionRoot', 'Type', 'Expiration',
                                                 'Strike', 'Last', 'Bid', 'Ask', 'Volume', 'OpenInterest',
                                                 'T1OpenInterest']]
                            lst_of_tuples = [tuple(row.values) for _, row in relevant.iterrows()]
                            sql_insertion = 'INSERT INTO ' + name + ' VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)'
                            self.cursor.executemany(sql_insertion, lst_of_tuples)
                            self.conn.commit()

    def close(self):
        self.conn.close()


if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)
    tables_to_create = ['FB', 'AAPL', 'NFLX', 'NVDA', 'MSFT', 'INTC', 'SPY']
    db = Database()
    db.create(tables_to_create)
    db.close()
