from keras.models import Sequential
from keras.layers import Dense, Dropout, Conv2D, MaxPooling2D,  Activation, Flatten
from keras.optimizer_v2.adam import Adam

from collections import deque

import numpy as np
import random



REPLAY_MEMORY_SIZE = 50_000
MIN_REPLAY_SIZE = 1_000
MINIBATCH_SIZE = 64
UPDATE_TARGET_EVERY = 5
DISCOUNT = 0.99


class DQNAgent(object):
    
    def __init__(self, env):
        # set environment
        self.env = env
        
        # main model, gets trained every step
        self.model = self.create_model()
        
        # target model, this is we want .predict against every step
        # try to bring sanity to randomness
        self.target_model = self.create_model()
        self.target_model.set_weights(self.model.get_weights())
        
        self.replay_memory = deque(maxlen = REPLAY_MEMORY_SIZE)
        self.target_update_counter = 0
    
    def create_model(self):
        model = Sequential()
        model.add(Conv2D(256, (3,3), input_shape=self.env.OBSERATION_SPACE_VALUES))
        model.add(Activation("relu"))
        model.add(MaxPooling2D(2,2))
        model.add(Dropout(.2))
        
        model.add(Conv2D(256, (3,3)))
        model.add(Activation("relu"))
        model.add(MaxPooling2D(2,2))
        model.add(Dropout(.2))
        
        model.add(Flatten())
        model.add(Dense(65))
        
        model.add(Dense(self.env.ACTION_SPACE_SIZE, activation="linear"))
        model.compile(loss="mse", optimizer=Adam(learning_rate=.001), metrics=['accuracy'])
        
        return model
    
    def update_replay_memory(self, transition):
        self.replay_memory.append(transition)
        
    def get_qs(self, state):
        return self.model.predict(np.array(state).reshape(-1, *state.shape)/255)[0]
    
    def train(self, terminal_state, step):
        if len(self.replay_memory) < MIN_REPLAY_SIZE:
            return
        
        minibatch = random.sample(self.replay_memory, MINIBATCH_SIZE)
        
        current_stats = np.array([transition[0] for transition in minibatch])/255
        current_qs_list = self.model.predict(current_stats)
        
        future_states = np.array([transition[3] for transition in minibatch])/255
        future_qs_list = self.model.predict(future_states)
        
        X = []
        y = []
        
        for index, (current_state, action, reward, future_states, done) in enumerate(minibatch):
            if not done:
                max_future_q = np.max(future_qs_list[index])
                new_q = reward + DISCOUNT * max_future_q
            
            else:
                new_q = reward
                
            current_qs = current_qs_list[index]
            current_qs[action] = new_q

            X.append(current_state)
            y.append(current_qs)
        
        self.model.fit(np.array(X)/255, np.array(y)/255, batch_size=MINIBATCH_SIZE, verbose=0, shuffle=False if terminal_state else None)
        
        if terminal_state:
            self.target_update_counter += 1
            
        if self.target_update_counter > UPDATE_TARGET_EVERY:
            self.target_model.set_weights(self.model.get_weights())
            self.target_update_counter = 0
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        