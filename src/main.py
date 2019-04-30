#!/usr/bin/env python3

import time

from lib.Gui import Gui
from lib.Game import Game

field = (0, 0, 30, 30)

game = Game(field)
gui = Gui(field, 50)

direction = 'r'

def up(event):
    game.snake.move_up()

def down(event):
    game.snake.move_down()

def left(event):
    game.snake.move_left()

def right(event):
    game.snake.move_right()

def quit_game(event):
    gui.running = False    
    
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
        game.update()
        game.draw(gui)
    
        time.sleep(0.5)