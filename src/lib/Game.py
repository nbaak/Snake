


class Game():
    
    # x1,y1, x2, y2
    def __init__(self, field = (0, 0, 30, 30)):
        self.field = field
        
    def point_is_in_field(self, point):
        if point[0] >= self.field[0] and point[0] <= self.field[2] and point[1] >= self.field[1] and point[1] <= self.field[3]:
            return True
        
        else:
            return False