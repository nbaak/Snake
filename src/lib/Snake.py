


class Snake:
    
    def __init__(self, coordinates = (5,5), size = 2, direction = 'r'):
        self.head = coordinates
        self.direction = direction
        self.body = []
        self.body.append(coordinates)
        self.grow = False
        
        for i in range(1,size+1):
            if direction == 'r':
                self.body.append((coordinates[0]-i,coordinates[1]))
            elif direction == 'l':
                self.body.append((coordinates[0]+i,coordinates[1]))
            elif direction == 'u':
                self.body.append((coordinates[0],coordinates[1]-i))
            elif direction == 'd':
                self.body.append((coordinates[0],coordinates[1]+i))
            else:
                pass            
            
    def move_right(self):
        if self.direction != 'l':
            self.direction = 'r'
            
    def move_left(self):
        if self.direction != 'r':
            self.direction = 'l'
        
    def move_up(self):
        if self.direction != 'd':
            self.direction = 'u'
        
    def move_down(self):
        if self.direction != 'u':
            self.direction = 'd'
         
    def eat(self):
        self.grow = True
            
    def update(self):
        old_body = self.body.copy()
        old_head = self.head
        
        if self.direction == 'r':
            self.head = (self.head[0] +1, self.head[1])
        elif self.direction == 'l':
            self.head = (self.head[0] -1, self.head[1])
        elif self.direction == 'u':
            self.head = (self.head[0]   , self.head[1] +1)
        elif self.direction == 'u':
            self.head = (self.head[0]   , self.head[1] -1)
        else:
            pass
        
        # move body...
        self.body = []
        self.body.append(self.head)
        self.body.extend(old_body[0:-1])
        
        if (self.grow):
            self.body.append(self.tail)
            self.grow = False
            
        self.tail = self.body[-1]
       
    def bite_self(self):
        return self.head in self.body[1:]
    
    def draw(self):
        pass
      