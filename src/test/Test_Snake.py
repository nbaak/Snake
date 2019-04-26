
import unittest

from lib.Snake import Snake

class Test_Snake(unittest.TestCase):
    
    def test_crate_snakes(self):
        s_r = Snake((5,5), 2, 'r')
        s_l = Snake((5,5), 2, 'l')
        s_u = Snake((5,5), 2, 'u')
        s_d = Snake((5,5), 2, 'd')

