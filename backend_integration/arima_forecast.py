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
  results_ARIMA.plot_predict(length-100,length+5)
  plt.show()
  x = results_ARIMA.forecast(steps=5)
  print(x[0])
  print(x[2])
  plt.plot(x[0])
  plt.plot(x[1])


  plt.show()


# forecasting("date_price_sales.csv")