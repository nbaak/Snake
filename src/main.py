#!/usr/bin/env python3

import time
import asyncio

from gui.Gui import Gui
from lib.Direction import Direction
from lib.Game import Game
from lib.Pathfinder import Pathfinder

field = (0, 0, 30, 20)

game = Game(field)
gui = Gui(field, 25)
pf = Pathfinder(game, game.snake.head, game.food.position)
direction = Direction.RIGHT

def up(event):
    game.direction = Direction.UP

def down(event):
    game.direction = Direction.DOWN
    print (10*'############\n')

def left(event):
    game.direction = Direction.LEFT
    
def right(event):
    game.direction = Direction.RIGHT

def quit_game(event):
    gui.running = False    
    
gui.bind('w', up)
gui.bind('s', down)
gui.bind('a', left)
gui.bind('d', right)
gui.bind('q', quit_game)

async def main():
    while gui.running:
        gui.reset()
        game.new_snake()
        game.new_food()
        
        while game.rules() and gui.running:
            #set_direction()
            gui.update_loop()
            game.update()
            
            #pf.random_step()
            pf.find_path(game.snake.head, game.food.position)
            pf.draw(gui)
            
            game.draw(gui)
            
            await asyncio.sleep(.2) # dunno it this is better than the old time.sleep()
        
        
        
if __name__ == "__main__":
    asyncio.get_event_loop().run_until_complete(main())
        