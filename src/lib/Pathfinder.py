import math
import random

from lib.point_to_order import point_to_order
from lib.Direction import Direction

class Pathfinder:
    
    def __init__(self, game, current = None, target = None):
        self.game = game
        self.current_position = current
        self.target_position = target
        
        self.path = []
        self.old_path = None
        self.steps_done = 0
        
        # for randomization
        self.directions = []
        self.directions.append(Pathfinder._next_up)
        self.directions.append(Pathfinder._next_down)
        self.directions.append(Pathfinder._next_left)
        self.directions.append(Pathfinder._next_right)
        
    def _update (self, current, target):
        self.current_position = current
        self.target_position = target
        
    def find_path (self, current, target):
        self._update(current, target)
        
        # clear
        self.steps_done = 0
        self.old_path = self.path.copy()
        self.path.clear()
        
        # do it
        try:
            if self._solve_path(self.current_position):
                self.path.pop(0)
            else:
                self.path.clear()
        except:
            self.path.clear()
            print ("no possible path")
            
    def get_next_step(self, current, target):
        self.find_path(current, target)

        if (len(self.path) > 0):
            next = self.path[0]
        else:
            next = None 
            
        print (f"{current}:{next}")
        return next
    
    def random_step(self):
        func = random.choice(self.directions)
        next = func(self.current_position)
        print ("random point: {}".format(next))
    
    def follow(self, current_direction):
        if len(self.path) > 0:
            move = point_to_order(self.game.snake.head, self.path[0], current_direction)
        
        else:
            dirs = Direction.get_standard_directions()
            eyes = self.game.snake.eyes()
            
            for d, e in zip(Direction.get_standard_directions(), eyes):
                if not e:
                    dirs.remove(d)              
            try:
                move = random.choice(dirs)
            except:
                move = random.choice(Direction.get_standard_directions())
            
        
        print(move)
        self.game.snake.direction = move
        return move
    
        
    def draw(self, gui):
        for p in self.old_path:
            gui.draw_square(point=p, color='#ffffff')
            
        for p in self.path:
            gui.draw_square(point=p, color='#ffa500')
            
    @staticmethod
    def _distance_between(a, b):
        return math.sqrt((a[0]-b[0]) * (a[0]-b[0])
                        +(a[1]-b[1]) * (a[1]-b[1]))
    
    @staticmethod
    def _next_up(current):
        return (current[0]+0, current[1]-1)
    
    @staticmethod
    def _next_down(current):
        return (current[0]+0, current[1]+1)
    
    @staticmethod
    def _next_left(current):
        return (current[0]-1, current[1]-0)
    
    @staticmethod
    def _next_right(current):
        return (current[0]+1, current[1]+0)
    
    def _solve_path(self, current):
        if self.steps_done >= self.game.max_amount_of_steps:
            return False
        
        self.steps_done += 1
        self.path.append(current)
        if (current == self.target_position):
            #print ("found in: " + str(self.steps_done) + " steps")
            return True
        
        directions = []
        directions.append( Pathfinder._next_up(current) )    # up
        directions.append( Pathfinder._next_down(current) )  # down
        directions.append( Pathfinder._next_left(current) )  # left
        directions.append( Pathfinder._next_right(current) ) # right
        
        # find closest 'next' point
        next_point_distances = []
        next_points = {}
        
        # go through all directions        
        for direction in directions:
            # add if possible        
            if (self.game.check_field(direction) and (direction not in self.path)):
                distance = Pathfinder._distance_between(self.target_position, direction)
                next_point_distances.append(distance)
                next_points[distance] = direction
                    
        next_point_distances.sort()

        for distance in next_point_distances:
            if self._solve_path(next_points[distance]):
                return True
            else:
                if len(self.path) >= 1:
                    self.path.pop()
                    self.steps_done -= 1
            
        self.path.pop()
        return False
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            