import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime
from statsmodels.tsa.arima_model import ARIMA
from matplotlib.pylab import rcParams
import warnings
warnings.simplefilter(action='ignore', category=Warning)
rcParams['figure.figsize'] = 10,6


def forecasting(filename):
  # dataset = pd.read_csv(filename)
  dataset = filename

  dataset['Date'] = pd.to_datetime(dataset['Date'],infer_datetime_format=True)
  dataset = dataset[['Date','Price']]
  indexedDataset = dataset.set_index(['Date'])
  indexedDataset = indexedDataset.fillna(method='ffill')

  #arima
  model  = ARIMA(indexedDataset,order=(2,1,2))
  results_ARIMA = model.fit(disp=-1)

  # predictions_ARIMA_diff = pd.Series(results_ARIMA.fittedvalues,copy=True)

  # #convert to cumulative sum
  # predictions_ARIMA_diff_cumsum = predictions_ARIMA_diff.cumsum()

  # predictions_ARIMA_log = pd.Series(indexedDataset_logScale['Price'][0],index=indexedDataset_logScale.index)
  # predictions_ARIMA_log = predictions_ARIMA_log.add(predictions_ARIMA_diff_cumsum,fill_value=0)
  # predictions_ARIMA_log.head()

  # predictions_ARIMA = np.exp(predictions_ARIMA_log)
  length = len(dataset)
  results_ARIMA.plot_predict(length-80,length+5)
  plt.savefig('forecast.png')
  # plt.show()

  steps_ahead = 5

  previous_sales = dataset[-80:]
  previous_sales = list(previous_sales['Price'])

  x = results_ARIMA.forecast(steps=steps_ahead)
  # for i in range(stepsAhead):
  #   series.loc[len(series)] = forecastArray[0][i]\

  print('----------------results-----------------------')
  print(results_ARIMA)

  print(x[0])
  print(x[2])
  plt.plot(x[0])
  plt.plot(x[1])

  min_max_sales = x[2]


  possible_min_sales = []
  possible_max_sales = []

  for i in range(steps_ahead):
    possible_min_sales.append(min_max_sales[i][0])
    possible_max_sales.append(min_max_sales[i][1])


  # plt.show()

  print(possible_min_sales)
  print(possible_max_sales)

  print(previous_sales)





  return list(x[0]),possible_min_sales,possible_max_sales,previous_sales


# forecasting("date_price_sales.csv")