import sympy
import quandl
import datetime
import numpy as np
from scipy.stats import norm
from scipy.optimize import newton
from option.data import Database


class ImpliedVol:
    def __init__(self):
        pass

    def evaluate(self, vol, type, underlying_price, strike, int_rate, yrs_to_expiry, price):
        model = bsm(vol, type, underlying_price, strike, int_rate, yrs_to_expiry)
        return price - model

    def back_out(self, type, price, underlying_price, strike, yrs_to_expiry):
        int_rate = quandl.get("FRED/DFF")
        iv = newton(func=self.evaluate,
                    x0=np.random.random(),
                    args=(type, underlying_price, strike, int_rate, yrs_to_expiry, price))
        return iv


def bsm(vol, type, underlying_price, strike, int_rate, yrs_to_expiry):
    d1 = (np.log(underlying_price / strike) + ((int_rate + ((vol ** 2) / 2)) * yrs_to_expiry)) / \
         (vol * np.sqrt(yrs_to_expiry))
    d2 = d1 - vol * np.sqrt(yrs_to_expiry)
    if type == 'call':
        return underlying_price * norm.cdf(d1) - strike * np.exp(-int_rate * yrs_to_expiry) * norm.cdf(d2)
    else:
        return -underlying_price * norm.cdf(-d1) - strike * np.exp(-int_rate * yrs_to_expiry) * norm.cdf(d2)


def _bsm_derivative():
    underlying_price = sympy.Symbol('S0')
    strike = sympy.Symbol('K')
    int_rate = sympy.Symbol('r')
    yrs_to_expiry = sympy.Symbol('t')
    vol = sympy.Symbol('o')
    raise NotImplementedError


if __name__ == '__main__':
    names = ['AAPL']
    db, IV = Database(), ImpliedVol()
    opt_data = db.extract(name='FB')
    db.close()

    for row in opt_data:
        underlying_price = row[1]
        type = row[3]
        expiry = row[4].strptime('%d/%m/%Y')
        strike = row[5]
        last = row[6]
        yrs_to_expiry = (expiry - datetime.datetime.today()).days / 365
        iv = IV.back_out(type, last, underlying_price, strike, yrs_to_expiry)
