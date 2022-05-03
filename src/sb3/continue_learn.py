import os
import sys
import gym

sys.path.append(os.path.abspath(os.path.join(os.getcwd(), os.pardir)))

from stable_baselines3 import PPO as Algorithm
from sb3.SnakeEnv import SnakeEnv
from lib.Game import Game

from sb3.config import *

N = 20
game = Game(field=(0,0,N,N))
env = SnakeEnv(game)
env.reset()

model = Algorithm.load(in_model_path, env=env)

for iteration in range(300):
    model.learn(total_timesteps=TIMESTEPS, reset_num_timesteps=False, tb_log_name=OUT_FILE_NAME)
    model.save(f"{out_models_dir}/{TIMESTEPS*iteration}")