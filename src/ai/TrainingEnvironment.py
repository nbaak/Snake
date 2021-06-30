import numpy as np
from lib.Game import Game
from lib.Direction import Direction
from cv2 import cv2
from PIL import Image


WHITE = (255,255,255)
BLACK = (0,0,0)
RED   = (0,0,255)
BLUE  = (255,0,0)
GREEN = (0,255,0)

class TrainingEnvironment(object):
    
    def __init__(self, game, reward = 10, penalty = 20, epsilon = 0.9, decay = 0.9988, learning_rate = 0.1, discount = 0.95):
        self.game = game     
        self.steps_without_scoring = 0
        
        self.reward = reward
        self.penalty = penalty
        self.epsilon = epsilon
        self.decay = decay
        
        self.OBSERATION_SPACE_VALUES = self.observation_matrix().shape
        self.ACTION_SPACE_SIZE = 4
              
    def reset(self):
        self.game.reset()
        self.steps_without_scoring = 0
        return self.observation_matrix()
    
    def get_game_score(self):
        return self.game.get_score()
    
    def step(self, action):
        score_before = self.get_game_score()
        
        self.game.direction = Direction(action)
        self.game.update()
        
        done = not self.game.rules()        
        score_after = self.get_game_score()
        
        observation = self.observation_matrix()
            
        score = score_after - score_before        
        
        if score == 0:
            self.steps_without_scoring += 1
        else:
            reward = 50
            self.steps_without_scoring = 0
            
        if self.steps_without_scoring == 300:
            reward = -300
            done = True
        
        if not done:
            reward = 5
        
        if score == 0 and done:
            reward = -200
        
        
        return (observation, reward, done)
    
    def render(self):
        img = self.drawable_observation_matrix()
        img = img.resize((300,300))
        cv2.imshow(f"snake", np.array(img))
        cv2.waitKey(100)

    def observation_matrix(self):
        observation = np.zeros((self.game.field_height+2, self.game.field_width+2, 1), dtype=np.uint8)

        #borders
        for i in range(self.game.field_height+2):
            observation[i, 0, 0] = 1.0
            observation[i, self.game.field_width+1, 0] = 1.0
            
        for i in range(self.game.field_width+2):
            observation[0, i, 0] = 1.0
            observation[self.game.field_height+1, i, 0] = 1.0
        
        # snake body
        for row, col in self.game.snake.body[1:]:
            observation[col+1, row+1, 0] = 1.0
            
        # snake head
        observation[self.game.snake.head[1]+1, self.game.snake.head[0]+1, 0] = 1.0        
            
        # food
        observation[self.game.food.position[1]+1, self.game.food.position[0]+1, 0] = -1.0
                        
        #with np.printoptions(threshold=np.inf):
        #    print(observation)
        
        return observation    
            
    def drawable_observation_matrix(self):
        observation = np.full((self.game.field_height+2, self.game.field_width+2, 3), WHITE, dtype=np.uint8)

        #borders
        for i in range(self.game.field_height+2):
            observation[i, 0] = BLACK
            observation[i, self.game.field_width+1] = BLACK
            
        for i in range(self.game.field_width+2):
            observation[0, i] = BLACK
            observation[self.game.field_height+1, i] = BLACK
        
        # snake body
        for row, col in self.game.snake.body[1:]:
            observation[col+1, row+1] = BLUE
            
        # snake head
        observation[self.game.snake.head[1]+1, self.game.snake.head[0]+1] = RED
            
        # food
        observation[self.game.food.position[1]+1, self.game.food.position[0]+1] = GREEN
                        
        #with np.printoptions(threshold=np.inf):
        #    print(observation)
        img = Image.fromarray(observation, 'RGB')
        return img
        
        
        
        
        
        
        
        
        