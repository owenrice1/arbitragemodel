import requests
import json
import matplotlib.pyplot as plt
import numpy as np
fig, ax = plt.subplots()
APIKey = ''

def extractvalues(openclose, sym, period, equity_or_fx, symbolA, symbolB):
    sym = []
    count = 0
    if equity_or_fx == 0:
        timeseries = 'Time Series (Daily)'
        sSymbol = '2. Symbol'
        APILINK = 'https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol='+symbolA+'&outputsize=full&apikey='+APIKey
    elif equity_or_fx == 1:
        timeseries = 'Time Series FX (Daily)'
        sSymbol = '2. From Symbol'
        APILINK = 'https://www.alphavantage.co/query?function=FX_DAILY&from_symbol='+symbolA+'&to_symbol='+symbolB+'&apikey='+APIKey
    

    dataset = (requests.get(APILINK)).json()
    print(dataset)
    symbol = dataset['Meta Data'][sSymbol]
    if openclose == 0:
        for date, values in dataset[timeseries].items():
            sym.append(dataset[timeseries][date]['1. open'])
            count += 1
            if count>period:
                break
    elif openclose == 1:
        for date, values in dataset[timeseries].items():
            sym.append(dataset[timeseries][date]['4. close'])
            count += 1
            if count>period:
                break
    return sym

StLN = extractvalues(1, sym= 'arStLN', period= 100, equity_or_fx = 0, symbolA = 'HSBA.LON', symbolB = '')
StNY = extractvalues(0, sym= 'arStNY', period= 100, equity_or_fx = 0, symbolA = 'HSBC', symbolB = '')
FxAB = extractvalues(0, sym= 'arFxAB', period= 100,equity_or_fx = 1, symbolA = 'GBP', symbolB = 'USD')

#print(StLN)
#print(StNY)
#print(FxAB)

def stockratio(StockA, StockB, FxAB):
    stockratio = (float(StockA)*float(FxAB))/float(StockB)
    return stockratio

arRatio = []
for i in range(0,len(StLN)-1, 1):
    arRatio.insert(0, stockratio(StLN[i], StNY[i], FxAB[i]))
    #if cr>rollingavg:
        #print(str(y) + "Stock A overpriced" + str(cr))
    #elif cr<rollingavg:
        # print(str(y) + "Stock B overpriced" + str(cr))
    #else:
        #print(str(y) + "No deviation of note") 
arRolling = []
arRollingAvg = []
for z in range(30,len(StLN), 1):
    for p in range(0,29, 1):
        cuanto = len(StLN)-z+p
        arRolling.append(stockratio(StLN[cuanto], StNY[cuanto], FxAB[cuanto]))
    arRollingAvg.append(sum(arRolling)/len(arRolling))
sumrat = 0
for e in range(0,29):
    sumrat+=arRatio[e]
    arRollingAvg.insert(e,(sumrat/(e+1)))
print(arRollingAvg)

plt.plot(arRatio)
plt.plot(arRollingAvg)

plt.show()