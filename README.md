# pystock
Simple way to get stock (pandas) object with historic data, several upper indicators, and several lower indicators. 

# Requirements
- Python 2.7
- Pandas/Numpy
- yahoo_finance

# Use
```
import Stock as stock

today = datetime.datetime.now().strftime('%Y-%m-%d')

AppleStockObject = stock.Stock(ticker='aapl', startDate='2015-01-01', endDate=today)
```

## Object Arguments

- Stock(ticker, startDate, endDate, window, cache, refresh)
- ticker - string, the symbol for the stock
- startDate - string, the starting date in the form 'YYYY-MM-DD'
- endDate - string, same as startDate
- window - integer, the size of the rolling window for technical indicators, default = 26
- cache - boolean, force the use of the cached file?
- refresh - boolean, force pull new data?

## Object Attribues 

- object.ticker
- object.startDate
- object.endDate
- object.indicatorWindow
- object.data - pandas table of stock data
- object.adjClosePrice
- object.closePrice
- object.highPrice - daily high
- object.lowPrice - daily low
- object.openPrice
- object.volume
- object.sma - simple moving average
- object.ema - exponential moving average
- object.rsi - relative strength
- object.stDev - volatility
- object.momentum
- object.macd
- object.macdsignalline
- object.macdhistogram
- object.upperband - Upper Bollinger Band
- object.lowerband - Lower BOllinger Band
- object.upperindicators - pandas table of upper indicators
- object.lowerindicators - pandas table of lower indicators
