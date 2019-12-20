import math
import random

class Pathfinder:
    
    def __init__(self, game):
        self.game = game
        self.snake = self.game.snake
        self.food = self.game.food.position
        self.field = game.field
        
        self.path = []
        self.old_path = None
        self.steps_done = 0
        
        # for randomization
        self.directions = []
        self.directions.append(Pathfinder._next_up)
        self.directions.append(Pathfinder._next_down)
        self.directions.append(Pathfinder._next_left)
        self.directions.append(Pathfinder._next_right)
        
    def _update (self):
        self.snake = self.game.snake
        self.food = self.game.food.position
        self.field = self.game.field
        
    def predict (self):
        self._update()
        
        # clear
        self.steps_done = 0
        self.old_path = self.path.copy()
        self.path.clear()
        
        # do it
        if self._solve_path(self.snake.head):
            pass
        else:
            self.path.clear()
        
    def random_step(self):
        func = random.choice(self.directions)
        next = func(self.snake.head)
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
        if self.steps_done >= self.game.max_amount_of_steps:
            return False
        
        self.steps_done += 1
        self.path.append(current)
        if (current == self.food):
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
                distance = Pathfinder._distance_between(self.food, direction)
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
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            