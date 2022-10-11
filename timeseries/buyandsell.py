#%% Getting some example data
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


