#!/usr/bin/env python3

import numpy as np
import cv2

from ai.DQNAgent import DQNAgent
from ai.TrainingEnvironment import TrainingEnvironment

from lib.Game import Game
from tensorflow import keras

EPISODES = 1_000 #20_000

epsilon = 1.00
EPSILON_DECAY = 0.99975
MIN_EPSILON = 0.001
MIN_REWARD = -200

SHOW_PREVIEW = True
MONITOR_SCORES = True
AGGREGATE_STATS_EVERY = 50

MODEL_NAME = "snake_test_02"
ep_rewards = [-200]


def replay_scores(video, index = 0, scores = 0):
    for img in video:
        img = img.resize((300,300))
        cv2.imshow(f"Replay {index} {scores}", np.array(img))
        cv2.waitKey(100)
        
    cv2.destroyWindow(f"Replay {index} {scores}")

def main():
    global epsilon
    game = Game(field=(0,0,10,10))
    env = TrainingEnvironment(game)
    agent = DQNAgent(env)
    try:
        agent.model.load_model(f"models/{MODEL_NAME}.model")
    except:
        print ("could not load model")
    
    for episode in range(1, EPISODES+1):
        episode_reward = 0
        step = 1
        
        current_state = env.reset()
        done = False        
        
        monitored_scores = []
        
        while not done:
            
            if np.random.random() > epsilon:
                action = np.argmax(agent.get_qs(current_state))
                
            else:
                action = np.random.randint(0, env.ACTION_SPACE_SIZE)
                
                
            new_state, reward, done = env.step(action)
            episode_reward += reward
            
            agent.update_replay_memory((current_state, action, reward, new_state, done))
            agent.train(done, step)
            
            current_state = new_state 
            step += 1
                
            if MONITOR_SCORES or (SHOW_PREVIEW and not episode % AGGREGATE_STATS_EVERY):
                monitored_scores.append(env.drawable_observation_matrix())
        
        if (MONITOR_SCORES and env.get_game_score() > 0) or (SHOW_PREVIEW and not episode % AGGREGATE_STATS_EVERY):
            print(f"Episode: {episode}, Reward: {episode_reward}, Score: {env.get_game_score()}")
            replay_scores(monitored_scores, episode, env.get_game_score())
        
        if episode_reward > 1:
            print(f"Episode: {episode}, Reward: {episode_reward}, Score: {env.get_game_score()}")
            
        ep_rewards.append(episode_reward)
        if not episode % AGGREGATE_STATS_EVERY == 0 or episode == 1:
            min_reward = min(ep_rewards[-AGGREGATE_STATS_EVERY:])
            max_reward = max(ep_rewards[-AGGREGATE_STATS_EVERY:])
            
            if min_reward > MIN_REWARD:
                #print("save model")
                agent.save_model(f"models/{MODEL_NAME}.model")
                
        if epsilon > MIN_EPSILON:
            epsilon *= EPSILON_DECAY
            epsilon = max(MIN_EPSILON, epsilon)
            
            
            
            
            

if __name__ == "__main__":
    main()
    
    