import math

class Pathfinder:
    
    def __init__(self, game):
        self.game = game
        self.snake = self.game.snake
        self.food = self.game.food.position
        self.field = game.field
        
        self.path = []
        self.old_path = None
        self.steps_done = 0
        
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
        if self.solve_path(self.snake.head):
            pass
        else:
            self.path.clear()
        
        
    def draw(self, gui):
        for p in self.old_path:
            gui.draw_square(point=p, color='#ffffff')
            
        for p in self.path:
            gui.draw_square(point=p, color='#ffa500')
            
    @staticmethod
    def _distance_between(a, b):
        return math.sqrt((a[0]-b[0]) * (a[0]-b[0])
                        +(a[1]-b[1]) * (a[1]-b[1]))
    
    def solve_path(self, current):
        if self.steps_done >= self.game.max_amount_of_steps:
            return False
        
        self.steps_done += 1
        self.path.append(current)
        if (current == self.food):
            #print ("found in: " + str(self.steps_done) + " steps")
            return True
        
        directions = []
        directions.append( (current[0] , current[1]-1) ) # up
        directions.append( (current[0] , current[1]+1) ) # down
        directions.append( (current[0]-1 , current[1]) ) # left
        directions.append( (current[0]+1 , current[1]) ) # right
        
        # find closest 'next' point
        next_point_distances = []
        next_points = {}
        
        # go through all directions        
        for direction in directions:
            # add if possible        
            if (self.game.check_field(direction)):
                distance = Pathfinder._distance_between(self.food, direction)
                next_point_distances.append(distance)
                next_points[distance] = direction
                    
        next_point_distances.sort()

        for distance in next_point_distances:
            if self.solve_path(next_points[distance]):
                return True
            else:
                if len(self.path) >= 1:
                    self.path.pop()
            
        return False
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            