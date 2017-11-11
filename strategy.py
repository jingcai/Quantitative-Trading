import pytz
import datetime
import pandas as pd
from ibapi.order import Order
from ibapi.contract import Contract


class UsoXle:
    def __init__(self):
        self.ids = []
        self.lots = 5
        self.params = pd.read_csv(r'C:/Users/JD/Google Drive/Quantitative Trading/Trading Params/UsoXle Params.csv', header=0, index_col=0)

        xleC, usoC = Contract(), Contract()
        xleC.secType, usoC.secType = 'STK', 'STK'
        xleC.symbol, usoC.symbol = 'XLE', 'USO'
        xleC.currency, usoC.currency = 'USD', 'USD'
        xleC.exchange, usoC.exchange = 'ARCA', 'ARCA'
        self.contracts = (xleC, usoC)

    def timeToCheck(self):
        eastern = pytz.timezone('US/Eastern')
        now = eastern.localize(datetime.datetime.now())
        if now > eastern.localize(datetime.datetime(year=now.year, month=now.month, day=now.day,
                                                    hour=16, minute=00, second=00)):
            print('Time now is', now.strftime('%d/%m/%Y %H:%M:%S %Z%z'), '. Markets have closed.')
            return False
        elif now > eastern.localize(datetime.datetime(year=now.year, month=now.month, day=now.day,
                                                    hour=00, minute=59, second=30)):
            print('Time now is', now.strftime('%d/%m/%Y %H:%M:%S %Z%z'), '. Signal checking will begin.')
            return True
        else:
            print('It is still too early to check for signals.')
            return False

    def checkSignal(self, xPrice, yPrice):
        currSpread = yPrice - self.params['OLS Beta', 'UsoXle'] * xPrice - self.params.loc['OLS Const', 'UsoXle']
        predictedSpread = self.params.loc['AR(1)', 'UsoXle'] * currSpread
        if predictedSpread > currSpread:
            print('Buy spread at', currSpread, 'for predicted up move to', predictedSpread)
            print('Buy XLE at', yPrice, 'Sell USO at', xPrice)

            xleO, usoO = Order(), Order()
            xleO.action, usoO.action = 'BUY', 'SELL'
            xleO.orderType, usoO.orderType = 'LMT', 'LMT'
            xleO.totalQuantity, usoO.totalQuantity = self.lots, self.lots
            xleO.lmtPrice, usoO.lmtPrice = yPrice, xPrice

        elif predictedSpread < currSpread:
            print('Sell spread at', currSpread, 'for predicted down move to', predictedSpread)
            print('Sell XLE at', yPrice, 'Buy USO at', xPrice)

            xleO, usoO = Order(), Order()
            xleO.action, usoO.action = 'SELL', 'BUY'
            xleO.orderType, usoO.orderType = 'LMT', 'LMT'
            xleO.totalQuantity, usoO.totalQuantity = self.lots, self.lots
            xleO.lmtPrice, usoO.lmtPrice = yPrice, xPrice

        else:
            print('No order.')
