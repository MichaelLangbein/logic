#%% Getting some example data
from email import feedparser
import yfinance as y

apple = y.Ticker('AAPL')
ahist = apple.history(period='max')



#%% Getting possible predictors
from sktime.registry import all_estimators

all_estimators(
    "forecaster", filter_tags={"capability:pred_int": True}, as_dataframe=True
)


# %% training
import pandas as p
from sktime.forecasting.base import ForecastingHorizon
from sktime.forecasting.arima import ARIMA

ahist.index.freq = ahist.index.inferred_freq
forecaster = ARIMA(order=[1, 1, 1])
horizon = ForecastingHorizon(
    [1, 2, 3],
    is_relative=True
)
forecaster.fit(y=ahist.Close, fh=horizon)

#%% predicting
fh = ForecastingHorizon(
    p.Index(p.date_range(ahist.index.max(), periods=7, freq=ahist.index.freq)),
    is_relative=False
)
prediction = forecaster.predict_interval(fh=fh)


#%%
gamma = 0.9
fee = 2.45  # price for buying stock;
s0 = -fee
S = [-3*fee, -2*fee, -1*fee, 0*fee, 1*fee, 2*fee, 3*fee, 'sold']

def reward(sNext, s, a):
    if a == 'sell':
        return sNext - s0
    else:
        return 0

def prob(sNext, s, a):
    pass

def endState(s):
    return s == 'sold'

def value(policy, s):
    if endState(s):
        return 0
    a = policy[s]
    v = 0
    for sNext in S:
        vNow = reward(sNext, s, a)
        vFut = gamma * value(policy, sNext)
        v += prob(sNext, s, a) * (vNow + vFut)
    return v


policies = [
    ['sell'],
    ['keep', 'sell'],
    ['keep', 'keep', 'sell'],
    ['keep', 'keep', 'keep', 'sell']
]

vMax = 0
for policy in policies:
    v = value(policy, s0)
    if v > vMax:
        vMax = v
        pOpt = policy
print(pOpt)
    