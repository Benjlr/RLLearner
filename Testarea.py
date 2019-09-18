from gym import spaces
import pandas as pd
import numpy as np
import Utils.ADFTester as adf
from  StockGym import TradingEnvironment

fd = pd.read_csv('C:/Temp/test.csv')
T = TradingEnvironment.TradingEnv(df=fd)
print(np.shape(T._next_observation))