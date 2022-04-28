
from lib.Direction import Direction

def point_to_direction(current_position,next_position):
    dir_x = next_position[0] - current_position[0]
    dir_y = next_position[1] - current_position[1]
    
    if dir_x > 0:
        return Direction.RIGHT
    if dir_x < 0:
        return Direction.LEFT
    
    if dir_y > 0:
        return Direction.DOWN
    if dir_y < 0:
        return Direction.UP
    
    return Direction.NONE
    