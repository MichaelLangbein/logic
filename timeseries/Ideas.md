# Day-trading

Objective: make gains in a ~month time-frame.




## Short term


## Tasks

1. Find one stock to invest in now
2. From my stocks, suggest one to sell soon

## Strategy

1. Find one stock to invest in now
    - Suggest this when there is a high change of some near-future price being higher than the current price plus fees.

2. From my stocks, suggest one to sell soon
    2.1. When no hope of recouping
    2.2. When likely peaked
    2.3. When already had a big win


## YFinance

```python
import yfinance as y

apple = y.Ticker("AAPL")

apple.info
apple.get_news()            # maybe do some sentiment analysis
apple.get_analysis()        # Shows estimated earnings, growth, and past trends
apple.get_recommendations() # From different firms

h = apple.history(period="max")

```