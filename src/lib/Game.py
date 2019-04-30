from lib.Snake import Snake
from lib.Food import Food

class Game():
    
    # x1,y1, x2, y2
    def __init__(self, field = (0, 0, 30, 30)):
        self.field = field
        self.snake = Snake()
        self.food = Food((7,5))
        
    def new_snake(self):
        self.snake = Snake()
        
    def new_food(self):
        self.food = Food()
        
    def point_is_in_field(self, point):
        if point[0] >= self.field[0] and point[0] <= self.field[2] and point[1] >= self.field[1] and point[1] <= self.field[3]:
            return True        
        else:
            return False
        
    def update(self):
        self.snake.update()
        
    def rules(self):
        # snake bites self
        if self.snake.bite_self():
            print ("snake died")
            return False      
                
        # snake eats
        if self.snake.head == self.food.position:
            print ("eating")
            self.snake.eat()
            self.food.replace(self.snake)
        
        # snake leaves area / pass through wall?
        if not self.point_is_in_field(self.snake.head):
            return False
        
        # starvation? 
        # tbd maybe
        return True
        
    def draw(self, gui):
        self.food.draw(gui)
        self.snake.draw(gui)
        
