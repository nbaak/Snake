import random

class Food:
    
    food_color = '#00ff00'
    
    def __init__(self, position = (0,0), max_x = 5, max_y = 5):
        self.max_x = max_x
        self.max_y = max_y
        self.position = position
        
    def set_gui(self, gui):
        self.gui = gui
        
    def _random_poimt(self, range = (30,30)):
        return (random.randint(0, range[0]), random.randint(0, range[1]))
        
    def replace(self, snake):
        p = self._random_poimt((self.max_x,self.max_y))
        while p in snake.body:
            p = self._random_poimt((self.max_x, self.max_y))
            
        self.position = p
        #self.draw(gui)
        
    def draw(self, gui):
        gui.draw_square(self.food_color, self.position)