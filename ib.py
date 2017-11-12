import strategy
import logging
from threading import Thread
from ibapi.client import EClient
from ibapi.wrapper import EWrapper, iswrapper


class IdHandler:
    def __init__(self):
        self.id = 0

    def nxtId(self):
        self.id += 1
        return self.id


class Ib(EClient, EWrapper):
    def __init__(self, ip, portId, clientId):
        EWrapper.__init__(self)
        EClient.__init__(self, wrapper=self)
        self.connect(ip, portId, clientId)

        self.strategyIds = {}
        self.idHandler = IdHandler()
        self.strategies = [strategy.UsoXle()]

        self.tradingSystem = Thread(target=self.run)
        self.tradingSystem.start()

    def checkStrategies(self):
        for s in self.strategies:
            if s.timeToCheck():
                for c in s.contracts:
                    reqId = self.idHandler.nxtId()
                    s.ids.append(reqId)
                    self.strategyIds[reqId] = None
                    logging.debug('NonOrderRequest', '#' + str(reqId), ':', 'Get data for', c.symbol)
                    self.reqMktData(reqId=reqId, contract=c, genericTickList='',
                                    snapshot=False, regulatorySnapshot=False, mktDataOptions=[])

    @iswrapper
    def tickPrice(self, reqId , tickType, price, attrib):
        super().tickPrice(reqId, tickType, price, attrib)
        self.strategyIds[reqId] = price
        for s in self.strategies:
            if reqId in s.ids:
                allValsRecvd = [self.strategyIds[id] is not None for id in s.ids]
                if np.all(allValsRecvd):
                    s.checkSignal()

    def cancelMktDataStreaming(self, reqId):
        self.cancelMktData(reqId)


if __name__ == '__main__':
    app = Ib(ip='127.0.0.1', portId=7496, clientId=1)
    app.checkStrategies()
