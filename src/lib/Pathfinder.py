import math
import random

class Pathfinder:
    
    def __init__(self, rules, current = None, target = None):
        self.rules = rules
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
                pass
            else:
                self.path.clear()
        except:
            self.path.clear()
            print ("no possible path")
        
    def random_step(self):
        func = random.choice(self.directions)
        next = func(self.current_position)
        print ("random point: {}".format(next))
        
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
        if self.steps_done >= self.rules.max_amount_of_steps:
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
            if (self.rules.check_field(direction) and (direction not in self.path)):
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
            
        self.path.pop()
        return False
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            