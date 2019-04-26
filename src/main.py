#!/usr/bin/env python3

from lib.Snake import Snake

s_r = Snake((5,5), 2, 'r')
s_l = Snake((5,5), 2, 'l')
s_u = Snake((5,5), 2, 'u')
s_d = Snake((5,5), 2, 'd')

s_r.body == [(5,5), (4,5), (3,5)]
s_r.direction == 'r'
s_r.body == [(5,5), (6,5), (7,5)]
s_r.body == [(5,5), (5,4), (5,3)]
s_r.body == [(5,5), (5,6), (5,7)]
         
print (s_r.body)