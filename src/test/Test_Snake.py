#!/usr/bin/env python3

import unittest

import lib
from lib.Snake import Snake

class Test_Snake(unittest.TestCase):
    
    def test_crate_snakes(self):
        s_r = Snake((5,5), 2, 'r')
        s_l = Snake((5,5), 2, 'l')
        s_u = Snake((5,5), 2, 'u')
        s_d = Snake((5,5), 2, 'd')

        self.assertTrue(s_r.body == [(5,5), (4,5), (3,5)], "body right direction")
        self.assertTrue(s_r.direction == 'r')
        self.assertTrue(s_r.body == [(5,5), (6,5), (7,5)], "body left direction")
        self.assertTrue(s_r.body == [(5,5), (5,4), (5,3)], "body up direction")
        self.assertTrue(s_r.body == [(5,5), (5,6), (5,7)], "body down direction")
         
