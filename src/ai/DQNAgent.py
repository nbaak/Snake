
from tensorflow.keras.models import Sequential, load_model
from tensorflow.keras.layers import Dense, Dropout, Conv2D, Dense, MaxPooling2D,  Activation, Flatten
from tensorflow.keras.optimizers import Adam

from collections import deque

import numpy as np
import random


UPDATE_TARGET_EVERY = 5


class DQNAgent(object):
    
    def __init__(self, env, max_value = 255, discount = .99, min_replay_size = 1_000, max_replay_size = 50_000, mini_batch_size = 64):
        # set environment
        self.env = env
        
        # main model, gets trained every step
        self.model = self.create_model()
        
        # target model, this is we want .predict against every step
        # try to bring sanity to randomness
        self.target_model = self.create_model()
        self.target_model.set_weights(self.model.get_weights())
        
        
        self.target_update_counter = 0
        self.max_value = max_value
        self.discount = discount
        self.max_replay_size = max_replay_size
        self.min_replay_size = min_replay_size
        self.mini_batch_size = mini_batch_size
        
        self.replay_memory = deque(maxlen = self.max_replay_size)
    
    def create_model(self):
        model = Sequential()
        model.add(Conv2D(256, (3,3), input_shape=self.env.OBSERATION_SPACE_VALUES))
        model.add(Activation("relu"))
        #model.add(MaxPooling2D(2,2))
        model.add(Dropout(.2))
        
        model.add(Conv2D(512, (3,3)))
        model.add(Activation("relu"))
        #model.add(MaxPooling2D(2,2))
        model.add(Dropout(.2))
        
        model.add(Conv2D(256, (3,3)))
        model.add(Activation("relu"))
        #model.add(MaxPooling2D(2,2))
        model.add(Dropout(.2))
        
        model.add(Flatten())
        model.add(Dense(64))
        
        model.add(Dense(self.env.ACTION_SPACE_SIZE, activation="linear"))
        model.compile(loss="mse", optimizer=Adam(learning_rate=.001), metrics=['accuracy'])
        
        return model
    
    def save_model(self, name = "Model.h5"):
        self.model.save(f"{name}")
    
    def load_model(self, name = "Model.h5"):
        self.model = load_model(f"{name}")
        self.target_model.set_weights(self.model.get_weights())    
    
    def update_replay_memory(self, transition):
        self.replay_memory.append(transition)
        
    def get_qs(self, state):
        return self.model.predict(np.array(state).reshape(-1, *state.shape)/self.max_value)[0]
    

    def train_model(self, terminal_state, minibatch, current_qs_list, future_qs_list):
        X = [] # feature set (the image)
        y = [] # actions
        
        for index, (current_state, action, reward, future_state, done) in enumerate(minibatch):
            if not done:
                max_future_q = np.max(future_qs_list[index])
                new_q = reward + self.discount * max_future_q
            else:
                new_q = reward
            current_qs = current_qs_list[index]
            current_qs[action] = new_q
            X.append(current_state)
            y.append(current_qs)
        
        self.model.fit(np.array(X) / self.max_value, np.array(y), batch_size=self.mini_batch_size, verbose=0, shuffle=False if terminal_state else None)

    def train(self, terminal_state, step):
        if len(self.replay_memory) < self.min_replay_size:
            return

        minibatch = random.sample(self.replay_memory, self.mini_batch_size)
        
        current_stats = np.array([transition[0] for transition in minibatch])/self.max_value
        current_qs_list = self.model.predict(current_stats)
        
        future_states = np.array([transition[3] for transition in minibatch])/self.max_value
        future_qs_list = self.target_model.predict(future_states)
        
        self.train_model(terminal_state, minibatch, current_qs_list, future_qs_list)
        
        if terminal_state:
            self.target_update_counter += 1
            
        if self.target_update_counter > UPDATE_TARGET_EVERY:
            self.target_model.set_weights(self.model.get_weights())
            self.target_update_counter = 0
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        