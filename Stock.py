
import datetime
import os
import pandas        as pd
import TechIndicator as ti
import Utilities     as utl

from yahoo_finance import Share


class Stock(object):

    """
    :summary This downloads
    :param ticker: stock ticker symbol
    :param daterange: range of dates
    :returns: pandas array of stock data from the date range
    """
    def __init__(self, ticker, startDate, endDate, window=26, cache=False, refresh=False):
        self.ticker = ticker
        self.startDate = startDate
        self.endDate = endDate
        self.indicatorWindow = window
        self.cache = cache
        self.refresh = refresh
        self.Data()
        self.SimpleIndicators()


    def Data(self):
        filename = 'cache/%s_%s_%s.csv' % (self.ticker, self.startDate, self.endDate)
        if (not self.cache) or self.refresh:
            today = datetime.datetime.now().strftime('%Y-%m-%d')
            if (not os.path.exists(filename)) or self.refresh:
                self.LiveData()
            else:
                lastModified = datetime.datetime.fromtimestamp(os.stat(filename).st_mtime).strftime('%Y-%m-%d')
                if (lastModified != today):
                    self.LiveData()
                else:
                    print 'Using cached stock data for "%s" from %s to %s.' % (self.ticker, self.startDate, self.endDate)
        else:
            print 'Using cached stock data for "%s" from %s to %s.' % (self.ticker, self.startDate, self.endDate)

        try:
            stockData = pd.read_csv(filename, index_col='Date',
                parse_dates=True, na_values=['nan'])
        except:
            print 'ERROR: Cached data for "%s" doesn\'t exist.' % self.ticker
            exit()

        self.data          = stockData.drop('Symbol', axis=1)
        self.adjClosePrice = stockData[['Adj_Close']]
        self.closePrice    = stockData[['Close']]
        self.highPrice     = stockData[['High']]
        self.lowPrice      = stockData[['Low']]
        self.openPrice     = stockData[['Open']]
        self.volume        = stockData[['Volume']]


    def LiveData(self):
        print
        print 'Retrieving "%s" stock data from YaHoo from %s to %s...' %(self.ticker, self.startDate, self.endDate)
        try:
            stockDataSetup     = Share(self.ticker)
            stockDataSetup     = stockDataSetup.get_historical(self.startDate, self.endDate)
            print '    ..."%s" stock data retrieved.' % self.ticker
        except:
            print 'ERROR: stock data not retrieved'
            print
            print 'Program Stopped.'
            exit()
        print 'Converting "%s" stock data to DataFrames.' % self.ticker
        stockDataSetup     = stockDataSetup[::-1]
        stockData          = pd.DataFrame(stockDataSetup)
        stockData['Date']  = pd.to_datetime(stockData['Date'])
        stockData          = stockData.set_index('Date')
        stockData          = stockData.apply(pd.to_numeric, errors='coerce')
        print '    ...converting finished'
        if not (os.path.exists('cache/')):
            os.mkdir('cache/')
        stockData.to_csv(("cache/%s_%s_%s.csv" % (self.ticker, self.startDate, self.endDate)))


    def SimpleIndicators(self):
        self.typical_price = self.data[['Close', 'High', 'Low']].mean(axis=1)
        self.sma    = ti.SMA(self.adjClosePrice, self.indicatorWindow)
        self.ema    = ti.EMA(self.adjClosePrice, self.indicatorWindow)
        self.rsi_close = ti.RSI(self.adjClosePrice, self.indicatorWindow)
        self.rsi_typical = ti.RSI(self.typical_price, self.indicatorWindow)
        self.rsi_closem = ti.RSIM(self.adjClosePrice, self.indicatorWindow)
        self.rsi_typicalm = ti.RSIM(self.typical_price, self.indicatorWindow)
        self.stDev  = ti.STDev(self.adjClosePrice, self.indicatorWindow)
        self.momentum = ti.Momentum(self.adjClosePrice, self.indicatorWindow)
        self.macd, self.macdsignalline, self.macdhistogram \
            = ti.MACDHistogram(self.adjClosePrice, self.indicatorWindow)
        self.upperbband, self.lowerbband\
            = ti.BBands(self.adjClosePrice, self.sma, self.indicatorWindow)
        self.upperindicators = utl.concatDataframes([
                                                    [self.sma],
                                                    [self.ema],
                                                    [self.upperbband],
                                                    [self.lowerbband]
                                                    ])
        self.lowerindicators = utl.concatDataframes([
                                                    [self.stDev],
                                                    [self.momentum],
                                                    [self.rsi_close],
                                                    [self.rsi_typical],
                                                    [self.rsi_closem],
                                                    [self.rsi_typicalm],
                                                    [self.macd]
                                                    ])
        self.sma.columns = ['SMA']
        self.ema.columns = ['EMA']
        self.rsi_close.columns = ['RSI Close']
        self.rsi_typical.columns = ['RSI Typical']
        self.rsi_closem.columns = ['RSI Close Modified']
        self.rsi_typicalm.columns = ['RSI Typical Modified']
        self.macd.columns = ['MACD']
        self.macdsignalline.columns = ['MACD Signal']
        self.macdhistogram.columns = ['MACD Histogram']
        self.upperbband.columns = ['Upper Band']
        self.lowerbband.columns = ['Lower Band']
        self.upperindicators.columns = ['SMA', 'EMA', 'Upper Band', 'Lower Band']
        self.lowerindicators.columns = ['Volatility', 'Momentum', 'RSI Close', 'RSI Typical', 'RSI Close Modified', 'RSI Typical Modified', 'MACD']