import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
# %matplotlib inline
from matplotlib.pylab import rcParams
rcParams['figure.figsize'] = 10,6

dataset = pd.read_csv("date_price_sales.csv")

dataset['Date'] = pd.to_datetime(dataset['Date'],infer_datetime_format=True)
dataset = dataset[['Date','Price']]
indexedDataset = dataset.set_index(['Date'])
indexedDataset = indexedDataset.fillna(method='ffill')

from datetime import datetime
indexedDataset.head(5)

# ## plot graph
# plt.xlabel("date")
# plt.ylabel("price")
# plt.plot(indexedDataset)
# plt.show()

#determining rolling stats
rolmean  = indexedDataset.rolling(window=12).mean()
rolstd = indexedDataset.rolling(window=12).std()
# print(rolmean,rolstd)

# #plot rolling stats

# orig = plt.plot(indexedDataset,color = "blue",label="Original")
# mean = plt.plot(rolmean,color="red",label="rolling mean")
# std = plt.plot(rolstd,color="black",label="rolling std")

# plt.legend(loc='best')
# plt.title('rolling mean and std')
# plt.show(block=False)

#perform dickey fuller test

from statsmodels.tsa.stattools import adfuller

print('results of dickey fuller test')
dftest = adfuller(indexedDataset['Price'],autolag='AIC')

dfoutput = pd.Series(dftest[0:4],index=['Test Statistic','p-value','#Lags Used','Number of Observations Used'])

for key,value in dftest[4].items():
  dfoutput['Critical value (%s)'%key] = value

# print(dfoutput)



#estimating trend
indexedDataset_logScale = np.log(indexedDataset)
# plt.plot(indexedDataset_logScale)
# plt.show()


# moving average and standard deviation
movingAverage = indexedDataset_logScale.rolling(window=12).mean()
movingstd = indexedDataset_logScale.rolling(window=12).std()
# plt.plot(indexedDataset_logScale)

# plt.plot(movingAverage,color='red')
# plt.show()


datasetLogScaleMinusMovingAverage = indexedDataset_logScale - movingAverage 
datasetLogScaleMinusMovingAverage.head(12)

#remove nan values
datasetLogScaleMinusMovingAverage.dropna(inplace=True)
datasetLogScaleMinusMovingAverage.head(10)


# stationarity test
from statsmodels.tsa.stattools import adfuller
def test_stationarity(timeseries):
  movingAverage = timeseries.rolling(window=12).mean()
  movingstd = timeseries.rolling(window=12).std()
  
  #plot rolling stats

  # orig = plt.plot(timeseries,color = "blue",label="Original")
  # mean = plt.plot(movingAverage,color="red",label="rolling mean")
  # std = plt.plot(movingstd,color="black",label="rolling std")

  # plt.legend(loc='best')
  # plt.title('rolling mean and std')
  # plt.show(block=False)

  #perform dickey fuller test

  print('results of dickey fuller test')
  dftest = adfuller(timeseries['Price'],autolag='AIC')

  dfoutput = pd.Series(dftest[0:4],index=['Test Statistic','p-value','#Lags Used','Number of Observations Used'])

  for key,value in dftest[4].items():
    dfoutput['Critical value (%s)'%key] = value

  # print(dfoutput)

test_stationarity(datasetLogScaleMinusMovingAverage)


exponentialDecayWeightedAverage = indexedDataset_logScale.ewm(halflife=12,min_periods=0,adjust=True).mean()
# plt.plot(indexedDataset_logScale)
# plt.plot(exponentialDecayWeightedAverage,color='red')
# plt.show()



datasetLogScaleMinusMovingExponentialDecayAverage = indexedDataset_logScale - exponentialDecayWeightedAverage
# 
datasetLogScaleMinusMovingExponentialDecayAverage.dropna(inplace=True)
test_stationarity(datasetLogScaleMinusMovingExponentialDecayAverage)



datasetLogDiffShifting = indexedDataset_logScale - indexedDataset_logScale.shift()
# plt.plot(datasetLogDiffShifting)
# plt.show()


datasetLogDiffShifting.dropna(inplace=True)
test_stationarity(datasetLogDiffShifting)




# acf and pacf plots:

from statsmodels.tsa.stattools import acf,pacf

lag_acf = acf(datasetLogDiffShifting,nlags = 20)
lag_pacf = pacf(datasetLogDiffShifting,nlags = 20,method='ols')

# #plot acf
# plt.subplot(121)
# plt.plot(lag_acf)
# plt.axhline(y=0,linestyle='--',color='gray')
# plt.axhline(y=-1.96/np.sqrt(len(datasetLogDiffShifting)),linestyle='--',color='gray')
# plt.axhline(y=1.96/np.sqrt(len(datasetLogDiffShifting)),linestyle='--',color='gray')
# plt.title('Autocorrelation function')
# plt.show()

# #plot pacf
# plt.subplot(122)
# plt.plot(lag_pacf)
# plt.axhline(y=0,linestyle='--',color='gray')
# plt.axhline(y=-1.96/np.sqrt(len(datasetLogDiffShifting)),linestyle='--',color='gray')
# plt.axhline(y=1.96/np.sqrt(len(datasetLogDiffShifting)),linestyle='--',color='gray')
# plt.title('Partial Autocorrelation function')
# plt.tight_layout()
# plt.show()



from statsmodels.tsa.arima_model import ARIMA

# AR model


model  = ARIMA(indexedDataset,order=(2,1,2))
results_AR = model.fit(disp=-1)
plt.plot(datasetLogDiffShifting)
plt.plot(results_AR.fittedvalues,color='red')
plt.title('RSS:%.4f'% sum((results_AR.fittedvalues-datasetLogDiffShifting['Price'])**2))
print('Plotting AR model')
plt.show()


#MA model

model  = ARIMA(indexedDataset,order=(0,1,2))
results_MA = model.fit(disp=-1)
plt.plot(datasetLogDiffShifting)
plt.plot(results_AR.fittedvalues,color='red')
plt.title('RSS:%.4f'% sum((results_AR.fittedvalues-datasetLogDiffShifting['Price'])**2))
plt.show()
print('Plotting MA model')



print("Before arima")

#arima
model  = ARIMA(indexedDataset,order=(2,1,2))
results_ARIMA = model.fit(disp=-1)
plt.plot(datasetLogDiffShifting)
plt.plot(results_AR.fittedvalues,color='red')
plt.title('RSS:%.4f'% sum((results_AR.fittedvalues-datasetLogDiffShifting['Price'])**2))
print('Plotting ARIMA model')

print("after arima")


predictions_ARIMA_diff = pd.Series(results_ARIMA.fittedvalues,copy=True)
print(predictions_ARIMA_diff.head())

print("after predictions_ARIMA_diff")

#convert to cumulative sum
predictions_ARIMA_diff_cumsum = predictions_ARIMA_diff.cumsum()
print(predictions_ARIMA_diff_cumsum)

print("after predictions_ARIMA_diff_cumsum")

predictions_ARIMA_log = pd.Series(indexedDataset_logScale['Price'][0],index=indexedDataset_logScale.index)
predictions_ARIMA_log = predictions_ARIMA_log.add(predictions_ARIMA_diff_cumsum,fill_value=0)
predictions_ARIMA_log.head()

print("after predictions_ARIMA_log")

predictions_ARIMA = np.exp(predictions_ARIMA_log)
plt.plot(indexedDataset)
plt.plot(predictions_ARIMA)
plt.show()


results_ARIMA.plot_predict(200,309)

x = results_ARIMA.forecast(steps=5)

print(x)

plt.plot([0,1,2,3,4])
plt.show()

