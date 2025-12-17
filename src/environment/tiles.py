# src/environment/tiles.py

TILE_SIZE = 32
T_AIR = 0       
T_EMPTY = 0
T_GROUND = 1    
T_WALL = 1   
T_PLAYER = 2
T_EXIT = 3   
T_HOLE = 4    
T_BUTTON = 5   
T_GATE = 6      
def is_solid(tile_id: int) -> bool:
    return tile_id in (T_GROUND, T_WALL, T_BUTTON, T_EXIT)

def get_tile_color(tile_id: int):
    if tile_id == T_GROUND:
        return (180, 180, 255)
    if tile_id == T_WALL:
        return (120, 120, 200)
    if tile_id == T_HOLE:
        return (30, 30, 50)
    if tile_id == T_EXIT:
        return (50, 220, 50)
    if tile_id == T_BUTTON:
        return (255, 210, 80)
    return None