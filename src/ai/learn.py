#!/usr/bin/env python3
import os
import numpy as np
import cv2

from ai.DQNAgent import DQNAgent
from ai.TrainingEnvironment import TrainingEnvironment

from lib.Game import Game

EPISODES = 25_000 #20_000

epsilon = 1.00
EPSILON_DECAY = 0.99975
MIN_EPSILON = 0.001
MIN_REWARD = -200

MONITOR_SCORES = True        # log at all
SHOW_PREVIEW = True          # show every N steps
REPLAY = True   # replay the last round
SAVE_REPLAY = True  # save replay as images

MONITOR_EVERY = 100


# Saving 
AGGREGATE_STATS_EVERY = 50
MODEL_NAME = "snake_test_02"
ep_rewards = [-200]


def replay_scores(video, index = 0, scores = 0):
    for img in video:
        img = img.resize((300,300))
        
        cv2.imshow(f"Replay {index} {scores}", np.array(img))
        cv2.waitKey(100)
        
    cv2.destroyWindow(f"Replay {index} {scores}")
    
def save_replay(video, episode = 0, scores = 0, reward = 0):
    index = 0
    path = f"./replays/{episode:05}_{scores:02}_{reward}/"
           
    if not os.path.exists(path):
        os.makedirs(path)        
    
    for img in video:
        img = img.resize((300,300))
        
        try:
            name = f"{index:09}.jpg"
            cv2.imwrite(path + name, np.array(img))
            #cv2.waitKey(0)
            #print (name)
        except Exception as e:
            print (e)           
        
        index += 1
        
    return path

def main():
    global epsilon
    game = Game(field=(0,0,10,10))
    env = TrainingEnvironment(game)
    agent = DQNAgent(env)
    try:
        agent.load_model(f"models/{MODEL_NAME}.model")
    except Exception as e:
        print ("could not load model")
        print (e)
    
    for episode in range(1, EPISODES+1):
        episode_reward = 0
        step = 1
        
        current_state = env.reset()
        done = False        
        
        monitored_scores = []
        rnd_step = 0
        ai_step = 0
        
        while not done:
            
            if np.random.random() > epsilon:
                ai_step += 1
                action = np.argmax(agent.get_qs(current_state))
                
            else:
                rnd_step += 1
                action = np.random.randint(0, env.ACTION_SPACE_SIZE)
                
            new_state, reward, done = env.step(action)
            episode_reward += reward
            
            agent.update_replay_memory((current_state, action, reward, new_state, done))
            agent.train(done, step)
            
            current_state = new_state 
            step += 1
                
            if REPLAY or SAVE_REPLAY:
                monitored_scores.append(env.preview_observation_matrix())
        
        score = env.get_game_score()
        if (MONITOR_SCORES and score > 0) or (SHOW_PREVIEW and not episode % MONITOR_EVERY):
            print(f"Episode: {episode}, Reward: {episode_reward}, Score: {score}, Epsilon {epsilon}, AI Steps: {ai_step}, RND Steps: {rnd_step}")         
            
            if REPLAY and score:
                replay_scores(monitored_scores, episode, score)
            
            if SAVE_REPLAY:
                print ("saved to:", save_replay(monitored_scores, episode, score, episode_reward))
            
        ep_rewards.append(episode_reward)
        if episode % AGGREGATE_STATS_EVERY == 0 or episode == 1:
            min_reward = min(ep_rewards[-AGGREGATE_STATS_EVERY:])
            max_reward = max(ep_rewards[-AGGREGATE_STATS_EVERY:])
            average_reward = sum(ep_rewards[-AGGREGATE_STATS_EVERY:]) / len(ep_rewards[-AGGREGATE_STATS_EVERY:])
            
            # save model
            agent.save_model(f"models/{MODEL_NAME}.model")
            print (f"min: {min_reward}, max: {max_reward}, avg: {average_reward}\n")
            
        if epsilon > MIN_EPSILON:
            epsilon *= EPSILON_DECAY
            epsilon = max(MIN_EPSILON, epsilon)
            
            
            
            
            

if __name__ == "__main__":
    main()
    
    