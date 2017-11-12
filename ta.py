def sma(data, window):
    cpy = data.copy()
    cpy['SMA(' + str(window) + ')'] = cpy['NAV'].rolling(window=window).mean()
    return cpy


def rsi(self, data, window):
    cpy = data.copy()
    cpy['Rets'] = cpy['NAV'].diff(1)
    cpy['gains'] = cpy['Rets'] * (cpy['Rets'] > 0).astype(int)
    cpy['loss'] = cpy['Rets'] * (cpy['Rets'] < 0).astype(int)
    cpy['Avg Gain'] = cpy['gains'].rolling(window=window).mean()
    cpy['Avg Loss'] = cpy['loss'].abs().rolling(window=window).mean()
    cpy['rs'] = cpy['Avg Gain'] / cpy['Avg Loss']
    cpy['rsi'] = 100 - 100 / (1 + cpy['rs'])
    return cpy


def bollinger(self, data, window, upper, lower):
    cpy = data.copy()
    cpy['SMA'] = cpy['NAV'].rolling(window=window).mean()
    cpy['Std'] = cpy['NAV'].rolling(window=window).std()
    cpy['Upper Bollinger'] = cpy['SMA'] + cpy['Std'] * upper
    cpy['Lower Bollinger'] = cpy['SMA'] - cpy['Std'] * lower
    return cpy
