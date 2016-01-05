
import pandas as pd


def normalize(data, dropna=True):
    if dropna:
        data       = data.dropna()
    normalizedData = data / data.ix[0,:]
    return normalizedData


def concatDataframes(data):
    featureData = []
    # featureTitle     = []
    for indicator in data:
        featureData.append(indicator[0])
        # featureTitle.append(indicator[1])
    concated    = pd.concat(featureData, axis=1)
    # concated.columns = featureTitle
    return concated


def futurePrice(data, forecast=5):
    #### negative is forward, positive is backward
    futurePrice = data.shift(-1*forecast, axis=0)
    # futurePrice.shift(periods=forecast, freq=DateOffset(days=-1*forcast))
    # futurePrice.index = futurePrice.index + pd.DateOffset(days=forecast)
    return futurePrice


# def removeHeader(data):
#
#     data.columns = ['']
#     return data