from stable_baselines3.common.env_checker import check_env
from sb3.SnakeEnv import SnakeEnv
from lib.Game import Game

game = Game(field=(0,0,10,10))
env = SnakeEnv(game)
# It will check your custom environment and output additional warnings if needed

print('Action Space' + str(env.action_space))
print('Observ Space' + str(env.observation_space))

obs_space = env.observation_space
obs = env.reset()

print()
print(f"observation: {obs} ({len(obs)})")

print(f"class: {type(obs)}, data type: {obs.dtype}")

print("example step return")
print(env.step(env.action_space.sample()))

check_env(env)

for _ in range(2):
    done = False
    obs = env.reset()
    
    while not done:
        env.render(sleep=100)
        action = env.action_space.sample()
        obs, reward, done, info = env.step(action)
        print(reward, env.game.snake.head)
        
        
        
        
        
        
        
        
        
        
        
        
        
    