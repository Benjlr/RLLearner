from gym import spaces
import pandas as pd
import numpy as np


thArray = pd.read_csv('C:/Temp/test.csv')
closes = thArray['assetClose']
print(closes[:4])
#returns = np.array[range(len(closes))]

from statsmodels.tsa.stattools import adfuller
X = closes.values
result = adfuller(X)
print('ADF Statistic: %f' % result[0])
print('p-value: %f' % result[1])
print('Critical Values:')
for key, value in result[4].items():
	print('\t%s: %.3f' % (key, value))



for i in range(1, len(closes)):
    returns.loc[i] = ((closes.loc[i]/closes.loc[i-1]) - 1)
    
print(returns[:4])