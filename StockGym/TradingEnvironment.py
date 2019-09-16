import StockGym.TradingActions
import random
import json
from gym import spaces
import pandas as pd
import numpy as np

MX_ACCNT_BLNCE = 2147483647
MX_SH = 2147483647
MX_OPN_PSTNS = 1
MX_STPS = 20000
INIT_ACCNT_BLNCE = 10000
LKBCK = 60
MX_RSK = 0.02
MX_SHRPE


class TradingEnvironment(gym.Env):
    """Copyright TruffleCo Industries 2019
        Authoriser: Benjamin Roberts (CEO, CTO, MD)
        Nothing to Truffle With"""  

    metadata = {'render.modes': ['human']}


    def __init__(self, df):
        super(TradingEnv, self).__init__()
        self.df = df
        self.reward_range = (0, MX_ACCNT_BLNCE)

        #0 initiate position, 1 move stop, 2 do nothing
        self.action_space = spaces.Box(
            low=np.array([0,0]), high = np.array([3,1]), dtype=np.float16)
        # may have to change this to reflect different obs space
        self.observation_space = spaces.Box(
            low=0, high=1, shape=(6,6), dtype=np.float16)


    def reset(self):
        self.balance = INIT_ACCNT_BLNCE
        self.net_worth = INIT_ACCNT_BLNCE
        self.max_net_worth = INIT_ACCNT_BLNCE
        self.min_net_worth = INIT_ACCNT_BLNCE
        self.shares_held = 0
        self.current_step = LOOKBACK + 1
        # additional state variables
        self.entering_long = False
        self.entering_short = False
        self.currently_long =False
        self.currently_short =False
        self.stop_value = None
        self.entry_price = None

        return self._next_observation()


    def _next_observation(self):
        # make sure to add new collumn values
        frame = np.array([
            self.df.loc[self.current_step: self.current_step + LKBCK, 'assetopen'].values,
            self.df.loc[self.current_step: self.current_step + LKBCK, 'assetHigh'].values,
            self.df.loc[self.current_step: self.current_step + LKBCK, 'assetLow'].values,
            self.df.loc[self.current_step: self.current_step + LKBCK, 'assetClose'].values,
            self.df.loc[self.current_step: self.current_step + LKBCK, 'assetKeltnerHigh'].values,
            self.df.loc[self.current_step: self.current_step + LKBCK, 'assetKeltnerLow'].values,
            self.df.loc[self.current_step: self.current_step + LKBCK, 'assetKeltnerMA'].values,
            self.df.loc[self.current_step: self.current_step + LKBCK, 'assetMACDFast'].values,
            self.df.loc[self.current_step: self.current_step + LKBCK, 'assetMACDSlow'].values,
            self.df.loc[self.current_step: self.current_step + LKBCK, 'assetSigma'].values,
            self.df.loc[self.current_step: self.current_step + LKBCK, 'indexopen'].values,
            self.df.loc[self.current_step: self.current_step + LKBCK, 'indexHigh'].values,
            self.df.loc[self.current_step: self.current_step + LKBCK, 'indexLow'].values,
            self.df.loc[self.current_step: self.current_step + LKBCK, 'indexClose'].values,
            self.df.loc[self.current_step: self.current_step + LKBCK, 'indexKeltnerHigh'].values,
            self.df.loc[self.current_step: self.current_step + LKBCK, 'indexKeltnerLow'].values,
            self.df.loc[self.current_step: self.current_step + LKBCK, 'indexKeltnerMA'].values,
            self.df.loc[self.current_step: self.current_step + LKBCK, 'indexMACDFast'].values,
            self.df.loc[self.current_step: self.current_step + LKBCK, 'indexMACDSlow'].values,
            self.df.loc[self.current_step: self.current_step + LKBCK, 'indexSigma'].values,
        ])

        obs = np.append(frame, [[
            self.balance / MX_ACCNT_BLNCE,
            self.max_net_worth / MX_ACCNT_BLNCE,
            self.shares_held / MAX_NUM_SHARES
        ]], axis=0)

        return obs


        def step(self, action):
            # Execute one time step within the environment
            self._take_action(action)
            self.current_step += 1

            minimum_length = len(self.df.loc[:, 'assetopen'].values) - (LKBCK + 1)
                        
            if self.current_step > minimum_length:
                self.current_step = 0
            else: do_trades()

            delay_modifier = (self.current_step / MX_STPS)
  
            reward = self.balance * delay_modifier
            done = self.net_worth <= 0
            obs = self._next_observation()
        return obs, reward, done, {}


        def  _take_action(self, action):
            current_price = random.uniforms(
                self.df.loc[self.current_step, "assetHigh"],
                self.df.loc[self.current_step, "assetLow"])
            action_type = action[0]
            amount = action[1]

            if action_type < 1:
                if amount > 0.5:
                    self.entering_long = True
                else:
                    self.entering_short = True
            elif action_type < 2:
                self.stop_value = amount

        self.net_worth = self.balance + self.shares_held * current_price

        if self.net_worth > self.max_net_worth:
            self.max_net_worth = net_worth


        def do_trades():

            open = self.df.loc[self.current_step, "assetopen"]
            high = self.df.loc[self.current_step, "assetHigh"]
            low = self.df.loc[self.current_step, "assetLow"]

            if self.entering_long & self.shares_held == None:
                self.shares_held, self.stop_value = enter_stock(
                    1, 
                    self.balance, 
                    self.df.loc[self.current_step, "ATR"], 
                    open)
                self.balance -= self.shares_held * open
                self.entry_price = open
                self.risked = (open - self.stop_value)
                self.trades.append({'step': self.current_step,
                    'stop': self.stop_value,
                    'type': "long"})

            elif self.entering_short & self.shares_held == None:
                self.shares_held, self.stop_value = enter_stock(
                    -1, 
                    self.balance, 
                    self.df.loc[self.current_step, "ATR"], 
                    open)
                self.balance -= self.shares_held * open
                self.entry_price = open
                self.risked = (open - self.stop_value)
                self.trades.append({'step': self.current_step,
                    'stop': self.stop_value,
                    'type': "short"})

            elif self.entering_long & low < self.stop_value:
                final_price = self.stop_value
                if open < self.stop_value:
                    final_price = open
                self.balance += self.shares_held * final_price
                final_r = (final_price - self.entry_price) / self.risked
                self.shares_held = None
                self.entering_long = False
                self.trades.append({'step': self.current_step,
                    'r_value': final_r,
                    'profit': final_r * self.risked,
                    'type': "exit_long"})

            elif self.entering_short & high > self.stop_value:
                final_price = self.stop_value
                if open > self.stop_value:
                    final_price = open
                self.balance += self.shares_held * final_price
                final_r = (final_price - self.entry_price) / self.risked
                self.shares_held = None
                self.entering_short = False
                self.trades.append({'step': self.current_step,
                    'r_value': final_r,
                    'profit': final_r * self.risked,
                    'type': "exit_short"})

        def _render_to_file(self, filename='render.txt'):
            # Render the environment to the screen
            profit = self.net_worth - INIT_ACCNT_BLNCE
            returns = self.net_worth / INIT_ACCNT_BLNCE - 1
            file = open(filename, 'a+')

            file.write(f'Step: {self.current_step}')
            file.write(f'Balance: {self.balance}')
            file.write(f'Shares held: {self.shares_held}')
            file.write(f'Net worth: {self.net_worth}')'
            file.write(f'Max net worth: {self.max_net_worth})')
            file.write(f'Profit: {profit}')
            file.write(f'Return: {returns}')

            file.close()


        def render(self, mode='live', title=None, **kwargs):
            if mode == 'file':
                self._render_to_file(kwargs.get('filename', 'render.txt'))
            elif mode == 'live':
                if self.visualisation == None:
                    self.visualisation = StockTradingGraph(self.df, title)

                if self.current_step > LKBCK:
                    self.visualisation.render(self.current_step, self.net_worth,
                        self.trades, window_size=LKBCK)