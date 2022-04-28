from enum import Enum

class Direction(Enum):
    UP = 0
    LEFT = 1
    DOWN = 2
    RIGHT = 3
    NONE = 5
    
    @staticmethod
    def get_standard_directions():
        directions = [Direction.UP, Direction.LEFT, Direction.DOWN, Direction.RIGHT]
        return directions.copy()
    
    @staticmethod
    def get_opposite_directuon(direction):
        if direction == Direction.UP:
            return Direction.DOWN
        
        elif direction == Direction.DOWN:
            return Direction.UP
        
        elif direction == Direction.LEFT:
            return Direction.RIGHT
        
        elif direction == Direction.RIGHT:
            return Direction.LEFT
        
        else:
            return Direction.NONE
        
      
      
    
if __name__ == "__main__":
    print(Direction(0))  