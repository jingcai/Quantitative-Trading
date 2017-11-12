"""

# from statsmodels.tsa.stattools import adfuller
# from statsmodels.tools.tools import add_constant
# from statsmodels.regression.linear_model import OLS

def adfTest(vals):
    adfResult = adfuller(vals, autolag='AIC', regression='c')
    print('ADF Statistic:', adfResult[0])
    print('P-Value:', adfResult[1])
    print('Used Lags:', adfResult[2])
    print('Critical Value (10%):', adfResult[4]['10%'])
    print('Critical Value (5%):', adfResult[4]['5%'])
    print('Critical Value (1%):', adfResult[4]['1%'])


def linRegWithAdf(x, y, addBias=True):
    model = fitLinReg(x, y, addBias)
    print(model.summary())
    adfTest(model.resid)
    return model


def fitLinRegSimpleRetsWithAdf(x, y, addBias=True):
    xRets = computeSimpleRet(x)
    yRets = computeSimpleRet(y)
    return linRegWithAdf(xRets, yRets, addBias)


def fitLinRegLogRetsWithAdf(x, y, addBias=True):
    xRets = computeLogRet(x)
    yRets = computeLogRet(y)
    return linRegWithAdf(xRets, yRets, addBias)
"""