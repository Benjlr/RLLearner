import StockGym.TradingActions as sg
from StockGraphing.StockTradingGraph import StockTradingGraph
from StockGraphing.TradingChart import TradingChart
import random
import json
import gym
from gym import spaces
import pandas as pd
import numpy as np
from gym import *
import pandas as pd
import numpy as np

from gym import spaces
from enum import Enum
from typing import List, Dict


class TradingEnv(gym.Env):
    """Copyright TruffleCo Industries 2019
        Authoriser: Benjamin Roberts (CEO, CTO, MD)
        Nothing to Truffle With"""  

    metadata = {'render.modes': ['human']}

    def __init__(self, 
                df, 
                init_balance: int = 10000, 
                max_rsk: float = 0.015): 
                
        super(TradingEnv, self).__init__()
        self.df = df
        self.start_balance = init_balance
        self.balance = init_balance
        self.risk = max_rsk
        self.entering_long = False
        self.entering_short = False
        self.currently_long =False
        self.currently_short =False
        self.stop_value = None
        self.entry_price = None
        self.entry_atr = None
        self.shares_held = 0
        self.lifetime_r = 0
        self.positioning = 0
        self.trades = {}
        self.reward_range = (-10, 10)
        self.num_trades = 0
        self.up_R = 0
        self.down_R= 0
        self.days_in= 0
        self.net_worths = [self.balance]
        self.net_worths.append(self.balance)
        self.visualisation = None

        #0 initiate position, 1 move stop
        #low = [ -1, 0] high = [ 1, 1]
        #COLUMN ONE
        #-1 = initiate sell
        #0 = do nothing
        #1, initiate buy
        
        #COLUMN TWO
        #0 = leave stop
        #1 = stop at previous close

        self.action_space = spaces.Box( np.array([-1,0.0]), np.array([1,1.0]))  # steer, gas, brake
        # may have to change this to reflect different obs space
        self.observation_space = spaces.Box(np.array([-1.0, -1.0, -1.0,-1.0,-1.0,
                                                        -1.0,-1.0,-50.0, -50.0, -5.0,
                                                        -1.0,  -1.0, -1.0, -1.0,
                                                        -1.0, -1.0, -1.0, -50.0, -50.0, -5.0, -1.0, 0.0]),
                                            np.array([1.0, 1.0, 1.0,1.0,1.0,
                                                        1.0,1.0,50.0, 50.0,5.0,
                                                        1.0, 1.0, 1.0, 1.0,
                                                        1.0, 1.0, 1.0, 50.0,50.0, 5.0, 1.0, 1.0]))
        #self.observation_space = spaces.Box(np.array([0, 0, 0, 0, 0,
         #                                               0,0,-50.0, -50.0, -5.0,
           #                                             0,  0, 0, 0,
             #                                           0, 0, 0, -50.0, -50.0, -5.0, -1.0, 0.0]),
            #                                np.array([10000.0, 10000.0, 10000.0,10000.0,10000.0,
                #                                        10000.0,10000.0,50.0, 50.0,5.0,
              #                                          10000.0, 10000.0, 10000.0, 10000.0,
                #                                        10000.0, 10000.0, 10000.0, 50.0,50.0, 5.0, 1.0, 1.0]))


    def reset(self):
        self.balance = self.start_balance
        self.current_step = 1
        # additional state variables
        self.entering_long = False
        self.entering_short = False
        self.currently_long =False
        self.currently_short =False
        self.stop_value = None
        self.entry_price = None
        self.entry_atr = None
        self.shares_held = 0
        self.lifetime_r = 0
        self.positioning = 0
        self.trades = []
        self.num_trades = 0
        self.up_R = 0
        self.days_in= 0
        self.down_R= 0
        self.visualisation = None
        self.net_worths = [self.balance]
        self.net_worths.append(self.balance)
        return self._next_observation()


    def _next_observation(self):

        current_row = self.df[self.current_step - 1 : self.current_step + 1]
        # make sure to add new collumn values
    

        stationary_open = (current_row['assetOpen'].values[1] / current_row['assetOpen'].values[0]) - 1
        stationary_high = (current_row['assetHigh'].values[1] / current_row['assetHigh'].values[0]) - 1
        stationary_low = (current_row['assetLow'].values[1] / current_row['assetLow'].values[0]) - 1
        stationary_close = (current_row['assetClose'].values[1] / current_row['assetClose'].values[0]) - 1
        stationary_keltnerhigh = (current_row['assetKeltnerHigh'].values[1] / current_row['assetKeltnerHigh'].values[0]) - 1
        stationary_keltnerlow = (current_row['assetKeltnerLow'].values[1] / current_row['assetKeltnerLow'].values[0]) - 1
        stationary_keltnerma = (current_row['assetKeltnerMA'].values[1] / current_row['assetKeltnerMA'].values[0]) - 1

        index_stationary_open = (current_row['indexopen'].values[1] / current_row['indexopen'].values[0]) - 1
        index_stationary_high = (current_row['indexHigh'].values[1] / current_row['indexHigh'].values[0]) - 1
        index_stationary_low = (current_row['indexLow'].values[1] / current_row['indexLow'].values[0]) - 1
        index_stationary_close = (current_row['indexClose'].values[1] / current_row['indexClose'].values[0]) - 1
        index_stationary_keltnerhigh = (current_row['indexKeltnerHigh'].values[1] / current_row['indexKeltnerHigh'].values[0]) - 1
        index_stationary_keltnerlow = (current_row['indexKeltnerLow'].values[1] / current_row['indexKeltnerLow'].values[0]) - 1
        index_stationary_keltnerma = (current_row['indexKeltnerMA'].values[1] / current_row['indexKeltnerMA'].values[0]) - 1
        

        frame = np.array([
            stationary_open,
            stationary_high,
            stationary_low,
            stationary_close,
            stationary_keltnerhigh,
            stationary_keltnerlow,
            stationary_keltnerma,
            current_row['assetMACDFast'].values[1],
            current_row['assetMACDSlow'].values[1],
            current_row['assetSigma'].values[1],
            index_stationary_open,
            index_stationary_high,
            index_stationary_keltnerlow,
            index_stationary_close,
            index_stationary_keltnerhigh,
            index_stationary_keltnerlow,
            index_stationary_keltnerma,
            current_row['indexMACDFast'].values[1],
            current_row['indexMACDSlow'].values[1],
            current_row['indexSigma'].values[1],
        ])

        """

        frame = np.array([
            current_row['assetOpen'].values[1],
            current_row['assetHigh'].values[1],
            current_row['assetLow'].values[1],
            current_row['assetClose'].values[1],
            current_row['assetKeltnerHigh'].values[1],
            current_row['assetKeltnerLow'].values[1],
            current_row['assetKeltnerMA'].values[1],
            current_row['assetMACDFast'].values[1],
            current_row['assetMACDSlow'].values[1],
            current_row['assetSigma'].values[1],
            current_row['indexopen'].values[1],
            current_row['indexHigh'].values[1],
            current_row['indexLow'].values[1],
            current_row['indexClose'].values[1],
            current_row['indexKeltnerHigh'].values[1],
            current_row['indexKeltnerLow'].values[1],
            current_row['indexKeltnerMA'].values[1],
            current_row['indexMACDFast'].values[1],
            current_row['indexMACDSlow'].values[1],
            current_row['indexSigma'].values[1],
        ])

        """

        if self.currently_long:
            stop_normalised = (self.df.loc[self.current_step, 'assetClose'] - self.stop_value) / self.entry_atr
        elif self.currently_short:
            stop_normalised = (self.stop_value - self.df.loc[self.current_step, 'assetClose'])  / self.entry_atr
        else: stop_normalised = 0

        obs = np.append(frame, np.array([self.positioning, stop_normalised]), axis = 0)
        return obs



    def step(self, action):
        # Execute one time step within the environment
        self._take_action(action)
        self.current_step += 1
        reward = self._do_trades()
        
        self.net_worths.append(self.balance)

        done = self.balance < 0 or self.current_step > 2430
        if done: 
            f=open("C:/Temp/results.txt", "a+")
            output = f'{self.balance}, {self.up_R}, {self.down_R}, {self.num_trades}'
            f.write(output)
            f.write("\n")
                
        obs = self._next_observation()
        
        return obs, reward, done, {}



    def  _take_action(self, action):
        
        action_type = action[0]
        stop_movement = action[1]
        
        if action_type > 0.33 and not self.currently_long and not self.currently_short:
            self.entering_long = True
        elif action_type < -0.33 and not self.currently_long and not self.currently_short:
            self.entering_short = True
        
        if self.currently_long:
            current_stop = self.stop_value
            current_close = self.df.loc[self.current_step, 'assetClose']
            self.stop_value = current_stop +  (current_close - current_stop ) * stop_movement
            
        elif self.currently_short:
            current_stop = self.stop_value
            current_close = self.df.loc[self.current_step, 'assetClose']
            self.stop_value = current_stop -  (current_stop - current_close) * stop_movement
            
        

    def _do_trades(self):
        openPrice = self.df.loc[self.current_step, "assetOpen"]
        highPrice = self.df.loc[self.current_step, "assetHigh"]
        lowPrice = self.df.loc[self.current_step, "assetLow"]

        if self.currently_long and lowPrice < self.stop_value:
            final_price = self.stop_value

            if openPrice < self.stop_value:
                final_price = openPrice
                
            self.balance += (final_price - self.entry_price) * self.shares_held
            final_r = (final_price - self.entry_price) / self.entry_atr
            self.lifetime_r += final_r                        
            self.up_R += final_r
            reward = final_r

            self.trades.append(
                {'step': self.current_step,
                'r_value': final_r,
                'profit': final_r * self.entry_atr*self.shares_held,
                'price':final_price,
                'type': "exit_long"})

            self.shares_held = None
            self.currently_long = False
            self.entry_atr = None
            self.stop_value = None
            self.entry_price = None
            self.positioning = 0
            self.days_in = 0
            self.num_trades += 1
            
        elif self.currently_short and highPrice > self.stop_value:
            final_price = self.stop_value

            if openPrice > self.stop_value:
                final_price = openPrice

            self.balance += (self.entry_price - final_price) * -self.shares_held
            final_r = (self.entry_price - final_price) / self.entry_atr
            self.lifetime_r += final_r
            self.down_R += final_r
            reward = final_r

            self.trades.append({'step': self.current_step,
                    'r_value': final_r,
                    'profit': final_r * self.entry_atr*self.shares_held,
                    'price':final_price,
                    'type': "exit_short"})

            self.shares_held = None
            self.currently_short = False
            self.entry_atr = None
            self.stop_value = None
            self.entry_price = None
            self.positioning = 0
            self.days_in = 0
            self.num_trades += 1
            
        elif self.entering_long:
            self.shares_held, self.stop_value = sg.enter_stock(1, 
                                                                self.balance, 
                                                                self.df.loc[self.current_step, "assetATR"], 
                                                                openPrice, 
                                                                self.risk)
            self.entry_price = openPrice
            self.entry_atr = (openPrice - self.stop_value)
            self.entering_long = False
            self.currently_long = True
            self.positioning = 1

            self.trades.append(
                    {'step': self.current_step,
                    'stop': self.stop_value,
                    'price':openPrice,
                    'type': "long"})

        elif self.entering_short:
            self.shares_held, self.stop_value = sg.enter_stock(-1,
                                                                self.balance, 
                                                                self.df.loc[self.current_step, "assetATR"], 
                                                                openPrice,
                                                                self.risk)                                                                
            self.entry_price = openPrice
            self.entry_atr = -(openPrice - self.stop_value)
            self.entering_short = False
            self.currently_short = True
            self.positioning = -1

            self.trades.append(
                {'step': self.current_step,
                'stop': self.stop_value,
                'price':openPrice,
                'type': "short"})

        if self.currently_long or self.currently_short:
            self.days_in += 1   

        return reward
                

    def _render_to_file(self, filename='render.txt'):
        # Render the environment to the screen
        profit = self.balance - self.start_balance
        returns = self.balance / self.start_balance - 1
        file = open(filename, 'a+')

        file.write(f'Step: {self.current_step}')
        file.write(f'Balance: {self.balance}')
        file.write(f'Shares held: {self.shares_held}')
        file.write(f'Profit: {profit}')
        file.write(f'Return: {returns}')

        file.close()


    def render(self, mode='human', close=False):
        if self.visualisation == None:
            self.visualisation = TradingChart(self.df)

        if self.current_step < len(self.df):
            self.visualisation.render(self.current_step, self.net_worths, None, self.trades)