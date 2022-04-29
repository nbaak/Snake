import os
import sys
import gym
import time

sys.path.append(os.path.abspath(os.path.join(os.getcwd(), os.pardir)))

from stable_baselines3 import PPO as Algorithm
from sb3.SnakeEnv import SnakeEnv
from lib.Game import Game

# Config
SAVENAME  = "PPOv6" # should contain the algorithm
SAVE_REPLAY = True

if SAVE_REPLAY:
    from sb3.save_image_to import save_images_as_animation
    SCREENSHOT_PATH = f"screenshots/{SAVENAME}"

    if not os.path.exists(SCREENSHOT_PATH):
        os.makedirs(SCREENSHOT_PATH)
N = 20
game = Game(field=(0,0,N,N))
env = SnakeEnv(game)
env.reset()

model_file = "2940000"
models_dir = f"models/{SAVENAME}"
model_path = f"{models_dir}/{model_file}"
model = Algorithm.load(model_path, env=env)

episodes = 50
for ep in range(episodes):
    obs = env.reset()
    done = False
    
    ep_score = 0
    score_before = 0
    score_after = 0
    frames = []
    
    while not done:
        if SAVE_REPLAY:
            frames.append(env.render(sleep=100))
        else:
            env.render(sleep=100)
              
        score_before = env.game.get_score()
        action, _ = model.predict(obs)
        obs, reward, done, info = env.step(action)
        
        score_after = env.game.get_score()
        #print(score_before, score_after, reward)
        
        if score_after > score_before:
            ep_score += 1
            print(f"{ep}-{ep_score} {reward}")
        
        
    if ep_score >= 10:
        print("SAVE")
        filename = f"{SCREENSHOT_PATH}/{int(time.time())}-{model_file}-{env.game.field_width}x{env.game.field_height}-{ep}-{ep_score}.gif"
        save_images_as_animation(frames, filename)
        
        
        
        