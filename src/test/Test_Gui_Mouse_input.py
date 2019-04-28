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
    
    
def mouse_click(event):
    x = int(event.x / square_size)
    y = int(event.y / square_size)
    p = (x,y)
    c = random_color()
    gui.draw_square(c, p)
    print ("{},{}: {}".format(x,y,c))
    
    
square_size = 50
field_size  = (0,0,30,30)

game = Game(field_size)
gui = Gui(field_size, square_size)
gui.bind("q", exit_game)
gui.bind("<Button-1>", mouse_click)

for x in range(30):
    for y in range(30):
        gui.draw_square('#ffffff', (x,y))

while gui.running:
    gui.update_canvas()
    #p = random_poimt((30,30))
    #color = random_color()
    #gui.draw_square(color, p)
    



