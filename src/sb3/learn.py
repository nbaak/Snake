import os
import sys
import gym

sys.path.append(os.path.abspath(os.path.join(os.getcwd(), os.pardir)))

from stable_baselines3 import PPO as Algorithm
from sb3.SnakeEnv import SnakeEnv
from lib.Game import Game

from sb3.config import *

# Config
#TIMESTEPS = 10_000  # save every n steps

SAVENAME = OUT_FILE_NAME

models_dir = out_models_dir

ensure_dirs()

game = Game(field=(0,0,20,20))
env = SnakeEnv(game)
env.reset()


model = Algorithm("MlpPolicy", env, verbose=1, tensorboard_log=logdir)

iteration = 0
#while True:
    #iteration += 1

for iteration in range(300):
    model.learn(total_timesteps=TIMESTEPS, reset_num_timesteps=False, tb_log_name=SAVENAME)
    model.save(f"{models_dir}/{TIMESTEPS*iteration}")
    
    
    
    
    
    
    
    
    
    
    
    