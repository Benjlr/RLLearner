import gym
import json
import datetime as dt
from stable_baselines.common.policies import MlpLstmPolicy
from stable_baselines.common.vec_env import DummyVecEnv
from stable_baselines import PPO2
import pandas as pd
from  StockGym import TradingEnvironment
import tensorflow as tf

fd = pd.read_csv('C:/Temp/test.csv')

# The algorithms require a vectorized environment to run
env = DummyVecEnv([
                  lambda: TradingEnvironment.TradingEnv(df=fd) ])
env.num_envs = 1
model = PPO2(MlpLstmPolicy, env, verbose=1, nminibatches=1)
model.learn(total_timesteps=100000)
obs = env.reset()

for i in range(2430):
  action, _states = model.predict(obs)
  obs, rewards, done, info = env.step(action)
  env.render()
