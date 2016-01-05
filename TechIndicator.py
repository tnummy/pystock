
import pandas as pd


def SMA(data, window=26):
    sma = pd.rolling_mean(data, window)
    return sma


def EMA(data, window=26):
    ema = pd.ewma(data, window)
    return ema


def MACDHistogram(data, windowLong=26, signalLineWindow=5):
    windowShort           = int(windowLong / 2)
    MACD                  = (EMA(data, windowLong) - EMA(data, windowShort))
    signalLine            = EMA(MACD, signalLineWindow)
    MACDHistogram         = MACD - signalLine
    return MACD, signalLine, MACDHistogram


def SignalLine(data, window=9, simple=False):
    if simple:
        signalLine = SMA(data, window)
    else:
        signalLine = EMA(data, window)
    return signalLine


def RSI(data, window=14):
    upData = data.shift(1, axis=0) - data
    upData[upData < 0] = 0
    upData = pd.rolling_mean(upData, window)

    downData = data.shift(1, axis=0) - data
    downData[downData > 0] = 0
    downData = abs(pd.rolling_mean(downData, window))
    rs = upData / downData
    rsi = (100 - (100 / (1 + rs)))
    return rsi


def Momentum(data, window=10):
    momentum = (data.shift(window, axis=0) - data)
    return momentum


def STDev(data, window=26):
    stdev = pd.rolling_std(data, window)
    return stdev


def BBands(data, sma, window=26):
    upperband = (sma + (2 * STDev(data, window)))
    lowerband = (sma - (2 * STDev(data, window)))
    return upperband, lowerband


def slowStochastic(data, window=14):
    slowStochastic = (data - pd.rolling_min(data, window)) / \
                        (pd.rolling_max(data, window) - pd.rolling_min(data, window))
    return slowStochastic
