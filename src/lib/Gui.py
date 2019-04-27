import tkinter

class Gui():
    
    #x1,y1, x2,y2
    def __init__(self, field = (0,0,10,10), square_size = 5):
        self.root = tkinter.Tk()
        self.square_size = square_size
        
        self.width = field[2] * self.square_size
        self.height = field[3] * self.square_size
        
        self.canvas = tkinter.Canvas(self.root, width=self.width, height=self.height)
        self.canvas.pack()
        
        
    def draw_square(self, color = '#ff0000', point = (0,0)):
        self.canvas.create_rectangle(point[0]*self.square_size,     point[1]*self.square_size, 
                                     (point[0]+1)*self.square_size, (point[1]+1)*self.square_size,
                                     fill=color)
        self.update_canvas()
    
    def main_loop(self):
        self.root.mainloop()
        
    def update_loop(self):
        self.root.update()
    
    def update_canvas(self):
        self.canvas.update()