#!/usr/bin/env python3

import time

from lib.Gui import Gui
from lib.Game import Game

field = (0, 0, 30, 30)

game = Game(field)
gui = Gui(field, 50)

direction = 'r'

def up(event):
    game.direction = 'u'

def down(event):
    game.direction = 'd'

def left(event):
    game.direction = 'l'
    
def right(event):
    game.direction = 'r'

def quit_game(event):
    gui.running = False    

def set_direction():
    if game.direction == 'u':
        game.snake.move_up()
        
    elif game.direction == 'd':
        game.snake.move_down()
        
    elif game.direction == 'l':
        game.snake.move_left()
        
    elif game.direction == 'r':
        game.snake.move_right()
        
    else:
        pass
    
gui.bind('w', up)
gui.bind('s', down)
gui.bind('a', left)
gui.bind('d', right)
gui.bind('q', quit_game)

while gui.running:
    gui.reset()
    game.new_snake()
    game.new_food()
    
    while game.rules() and gui.running:
        set_direction()
        game.update()
        game.draw(gui)
    
        time.sleep(0.5)
        
        
        
        
        
        