from lib.Snake import Snake
from lib.Food import Food
from lib.Direction import Direction

class Game():
    
    # x1,y1, x2, y2
    def __init__(self, field = (0, 0, 30, 30)):
        self.field = field
        self.field_width = field[2]
        self.field_height = field[3]
        self.max_amount_of_steps = self.field[2] * self.field[3]
        self.snake = Snake()
        self.food = Food((7,5), self.field_width, self.field_height)
        self._direction = Direction.RIGHT
        self.allow_movement = True
        
    def new_snake(self):
        self.snake = Snake()
        self.snake.set_is_in_field(self.point_is_in_field)
        
    def new_food(self):
        self.food.replace(self.snake)
        self.snake.sense_food(self.food)
        
    def point_is_in_field(self, point):
        if point[0] >= self.field[0] and point[0] <= self.field[2] and point[1] >= self.field[1] and point[1] <= self.field[3]:
            return True        
        else:
            return False
        
    def update(self):
        self.snake.update()
        self.allow_movement = True
        
    def rules(self):
        # snake bites self
        if self.snake.bite_self():
            print ("snake died")
            return False      
                
        # snake eats
        if self.snake.head == self.food.position:
            self.snake.eat()
            self.food.replace(self.snake)
            self.snake.sense_food(self.food)
        
        # snake leaves area / pass through wall?
        if not self.point_is_in_field(self.snake.head):
            return False
        
        # starvation? 
        # tbd maybe
        return True
    
    @property
    def direction(self):
        return self._direction
    
    @direction.setter
    def direction(self, direction):
        self._direction = direction
        if self.allow_movement:
            if direction == Direction.UP:
                self.snake.move_up()
                self.allow_movement = False
                
            elif direction == Direction.LEFT:
                self.snake.move_left()
                self.allow_movement = False
                
            elif direction == Direction.DOWN:
                self.snake.move_down()
                self.allow_movement = False
                
            elif direction == Direction.RIGHT:
                self.snake.move_right()
                
            
        else:
            pass
    
        
    def draw(self, gui):
        self.food.draw(gui)
        self.snake.draw(gui)
        
    def check_field(self, coordinates):
        if (self.point_is_in_field(coordinates) and not self.snake.bite_self(coordinates)):
            return True
        else:
            return False
        
    def get_score(self):
        return self.snake.meals
    