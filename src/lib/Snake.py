
from lib.Food import Food
from lib.Direction import Direction

import math

class Snake:
    head_color = '#ff0000'
    body_color = '#0000ff'
    path_color = '#cfcfcf'
    
    def __init__(self, coordinates = (5,5), size = 2, direction = Direction.RIGHT):
        self.head = coordinates
        self.direction = direction
        self.body = []
        self.body.append(coordinates)
        self.grow = False
        self.meals = 0
        self.food = Food()
        
        for i in range(1,size+1):
            if direction == Direction.RIGHT:
                self.body.append((coordinates[0]-i,coordinates[1]))
            elif direction == Direction.LEFT:
                self.body.append((coordinates[0]+i,coordinates[1]))
            elif direction == Direction.UP:
                self.body.append((coordinates[0],coordinates[1]-i))
            elif direction == Direction.DOWN:
                self.body.append((coordinates[0],coordinates[1]+i))
            else:
                pass
        
        self.tail = self.body[-1]
        self.trail = None  
            
    def move_right(self):
        if self.direction != Direction.LEFT:
            self.direction = Direction.RIGHT
            
    def move_left(self):
        if self.direction != Direction.RIGHT:
            self.direction = Direction.LEFT
        
    def move_up(self):
        if self.direction != Direction.DOWN:
            self.direction = Direction.UP
        
    def move_down(self):
        if self.direction != Direction.UP:
            self.direction = Direction.DOWN
         
    def eat(self):
        self.grow = True
        self.meals += 1
        #print (f"score: {self.meals}")
    
    def eyes(self):        
        up    = (self.head[0],   self.head[1]-1)
        left  = (self.head[0]-1, self.head[1])
        down  = (self.head[0],  self.head[1]+1)
        right = (self.head[0]+1, self.head[1])
        
        # up, left, down, right
        return (not self.bite_self(up)  and self.in_field(up),
                not self.bite_self(left) and self.in_field(left),
                not self.bite_self(down) and self.in_field(down),
                not self.bite_self(right) and self.in_field(right))
        
    def set_is_in_field(self, function):
        self.in_field = function    
    
    def update(self):
        old_body = self.body.copy()
        
        self._update_direction()
        
        # move body...
        self.body = []
        self.body.append(self.head)
        self.body.extend(old_body[0:-1])
        
        if (self.grow):
            self.body.append(self.tail)
            self.grow = False
            
        self.trail = self.tail
        self.tail = self.body[-1]

    def _update_direction(self):        
        if self.direction == Direction.RIGHT:
            self.head = (self.head[0] +1, self.head[1])
        elif self.direction == Direction.LEFT:
            self.head = (self.head[0] -1, self.head[1])
        elif self.direction == Direction.UP:
            self.head = (self.head[0]   , self.head[1] -1)
        elif self.direction == Direction.DOWN:
            self.head = (self.head[0]   , self.head[1] +1)
        else:
            pass
       
    def sense_food(self, food = None):
        self.food = food
    
    def bite_self(self, point = None):
        if point:
            return point in self.body[1:]
        else:
            return self.head in self.body[1:]
    
    def draw(self, gui):
        for part in self.body[1:]:
            gui.draw_square(self.body_color, part)
            
        gui.draw_square(self.path_color, self.trail)
        gui.draw_square(self.head_color, self.head)
        
    def distance_to_food(self):
        return math.sqrt((self.head[0]-self.food.position[0])*(self.head[0]-self.food.position[0])
                       + (self.head[1]-self.food.position[1])*(self.head[1]-self.food.position[1]))
        
        