#!/usr/bin/env python3

import time
import asyncio

from gui.Gui import Gui
from lib.Direction import Direction
from lib.Game import Game
from lib.Pathfinder import Pathfinder

field = (0, 0, 10, 7)

game = Game(field)
gui = Gui(field, 25)
pf = Pathfinder(game, game.snake.head, game.food.position)
direction = Direction.RIGHT


# game states
game_paused = False
auto_pilot = True

def up(event):
    game.direction = Direction.UP

def down(event):
    game.direction = Direction.DOWN

def left(event):
    game.direction = Direction.LEFT
    
def right(event):
    game.direction = Direction.RIGHT

def quit_game(event):
    gui.running = False
    
def game_pause(event):
    global game_paused
    print ("toggle pause")
    if game_paused:
        game_paused = False
    else:
        game_paused = True
  
def toggle_auto_pilot(event):
    global auto_pilot
    auto_pilot = not auto_pilot
    print(f"Auto Pilot is now {auto_pilot}")
    
gui.bind('w', up)
gui.bind('s', down)
gui.bind('a', left)
gui.bind('d', right)

gui.bind('p', game_pause)
gui.bind('q', quit_game)
gui.bind('e', toggle_auto_pilot)

async def main():
    while gui.running:
        gui.reset()
        game.new_snake()
        game.new_food()
        
        current_direction = Direction.RIGHT
        
        while game.rules() and gui.running:
            gui.update_loop()
            if not game_paused:                
                game.update()
                
                pf.random_step()
                next_point = pf.get_next_step(game.snake.head, game.food.position)
                if auto_pilot:                             
                    pf.follow()
                                
                pf.draw(gui)
                
                game.draw(gui)
            
            await asyncio.sleep(.2) # dunno it this is better than the old time.sleep()
        
        
        
if __name__ == "__main__":
    asyncio.get_event_loop().run_until_complete(main())
        