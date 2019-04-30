#!/usr/bin/env python3

from lib.Gui import Gui
from lib.Game import Game

import random

def random_color():
    rnd_color = lambda: random.randint(0,255)    
    return "#%02X%02X%02X" % (rnd_color(), rnd_color(), rnd_color())


def random_poimt(range = (30,30)):
    return (random.randint(0, range[0]), random.randint(0, range[1]))

def exit_game(event):
    print (event)
    gui.running = False
    #gui.root.destroy()
    
square_size = 50
field  = (0,0,30,30)

game = Game(field)
gui = Gui(field, square_size)
gui.bind("q", exit_game)

while gui.running:
    p = random_poimt((30,30))
    color = random_color()
    gui.draw_square(color, p)
    



