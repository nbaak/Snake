#!/usr/bin/env python3

import unittest

from lib.Snake import Snake

class Test_Snake(unittest.TestCase):
    
    def test_crate_snakes(self):
        s_r = Snake((5,5), 2, 'r')
        s_l = Snake((5,5), 2, 'l')
        s_u = Snake((5,5), 2, 'u')
        s_d = Snake((5,5), 2, 'd')

        self.assertTrue(s_r.body == [(5,5), (4,5), (3,5)], "body right direction")
        self.assertTrue(s_r.direction == 'r')
        self.assertTrue(s_l.body == [(5,5), (6,5), (7,5)], "body left direction")
        self.assertTrue(s_u.body == [(5,5), (5,4), (5,3)], "body up direction")
        self.assertTrue(s_d.body == [(5,5), (5,6), (5,7)], "body down direction")
        
    def test_snake_update(self):
        snake = Snake ((5,5),2, 'r')
        snake.update()        
        self.assertTrue(snake.body == [(6,5), (5,5), (4,5)], "updated once")
        
        snake.move_up()
    
    def test_snake_turn(self):
        snake = Snake ((5,5),2, 'r')
        snake.move_up()
        snake.update()
        self.assertTrue(snake.body== [(5,6),(5,5),(4,5)], "turn upward")
        
    def test_snake_eats(self):
        snake = Snake ((5,5),2, 'r')
        snake.eat()
        snake.update()
        self.assertTrue(snake.body == [(6,5),(5,5),(4,5),(3,5)], "snake grows")
        
        
         
