import numpy as np
from lib.Game import Game
from lib.Snake import Snake
from lib.Direction import Direction
import cv2
from PIL import Image
import gym
from gym import spaces
from collections import deque
    
SNAKE_LEN_GOAL = 30
WHITE = (255,255,255)
BLACK = (0,0,0)
RED   = (0,0,255)
BLUE  = (255,0,0)
GREEN = (0,255,0)
    
class SnakeEnv(gym.Env):
    """Custom Environment that follows gym interface"""

    def __init__(self, game):
        super(SnakeEnv, self).__init__()
        self.game = game
        self.snake = self.game.snake
        # Define action and observation space
        # They must be gym.spaces objects
        # Example when using discrete actions:
        self.action_space = spaces.Discrete(4)
        # Example for using image as input (channel-first; channel-last also works):
        
        self.prev_actions = deque(maxlen=SNAKE_LEN_GOAL)
        
        obs = self.reset()
        n_channels = len(obs)
        max_value = max(self.game.field)
        self.observation_space = spaces.Box(low=-max_value, high=max_value,
                                            shape=(n_channels,),
                                            dtype=np.int64)        
        

    def step(self, action):
        self.prev_actions.append(action)
        
        score_before = self.game.get_score()
        distance_before = self.game.snake.distance_to_food()
        
        self.game.direction = Direction(action)
        self.game.update()
        
        self.done = not self.game.rules()        
        score_after = self.game.get_score()
        distance_after = self.game.snake.distance_to_food()
        
        apple_reward = 0
        if score_after > score_before:
            apple_reward = 10000 #+ 100*self.game.get_score()
            self.rounds_without_score = 0
            
        total_reward = ((250 - self.snake.distance_to_food()) + apple_reward) / 100
                
        reward = total_reward - abs(self.prev_reward)
        self.prev_reward = total_reward
        
        if self.done:
            reward = -10
        
        self.rounds_without_score += 1
        
        observation = self.__observation()
        info = {}
        
        return observation, reward, self.done, info
    
    
    def reset(self):
        self.done = False
        self.rounds_without_score = 0
        self.prev_reward = 0
        
        self.game.reset()
        center_x = self.game.field_width // 2
        center_y = self.game.field_height // 2
        self.game.snake = Snake((center_x,center_y))
        
        for _ in range(SNAKE_LEN_GOAL):
            self.prev_actions.append(-1)
        
        observation = self.__observation()
                
        return observation  # reward, done, info can't be included
    
    
    def __observation(self):
        head_x, head_y = self.game.snake.head
        food_x, food_y = self.game.food.position
        
        d_x = food_x - head_x
        d_y = food_y- head_y
        
        self.observation = list(self.game.snake.head) + [d_x, d_y] + [len(self.snake.body)] + list(self.prev_actions)
        return np.array(self.observation)
    
    def render(self, mode='human', sleep=1):
        img = self.preview_observation_matrix()
        img = img.resize((300,300))
        cv2.imshow(f"snake", np.array(img))
        cv2.waitKey(sleep)
        return img
        
    def observation_matrix(self):
        return self.__observation_matrix_1dim()    
    
    def preview_observation_matrix(self):
        img = Image.fromarray(self.__observation_matrix_3dim(), 'RGB')
        return img
    
    def __observation_matrix_1dim(self):
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
            observation[col+1, row+1, 0] = 2.0
            
        # snake head
        observation[self.game.snake.head[1]+1, self.game.snake.head[0]+1, 0] = 3.0        
            
        # food
        observation[self.game.food.position[1]+1, self.game.food.position[0]+1, 0] = 4.0
        
        return observation    
            
    def __observation_matrix_3dim(self):
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
        #img = Image.fromarray(observation, 'RGB')
        return observation


