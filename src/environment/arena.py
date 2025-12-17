import pygame
from src.core import settings
from src.environment.tiles import (
    TILE_SIZE, T_GROUND, T_AIR, T_EXIT, T_BUTTON, T_HOLE, T_WALL, T_GATE
)

class Arena:
    def __init__(self, layout, rows=None, cols=None, start_pos=None, exit_pos=None, 
                 hole_positions=None, button_positions=None, 
                 falling_block_config=None):
        
        self.layout = layout
        self.rows = rows if rows is not None else len(layout)
        self.cols = cols if cols is not None else len(layout[0])
        
        self.start_pos = start_pos if start_pos else (1, 1)
        self.exit_pos = exit_pos
        self.origin_y = 0 
        
        # Posisi obstacle
        self.hole_positions = hole_positions if hole_positions else {}
        self.button_positions = button_positions if button_positions else {}
        
        # data config balok
        self.falling_block_config = falling_block_config 

    def draw_side(self, surface):
        self._draw_grid(surface)

    def draw_top(self, surface):
        self._draw_grid(surface)

    def _draw_grid(self, surface):
        for r in range(self.rows):
            for c in range(self.cols):
                tile = self.layout[r][c]
                rect = pygame.Rect(c * TILE_SIZE, r * TILE_SIZE, TILE_SIZE, TILE_SIZE)
                
                if tile == T_GROUND or tile == T_WALL:
                    pygame.draw.rect(surface, (100, 100, 100), rect)
                elif tile == T_EXIT:
                    pygame.draw.rect(surface, (0, 255, 0), rect)
                elif tile == T_BUTTON:
                    pygame.draw.rect(surface, (0, 200, 200), rect)
                    pygame.draw.rect(surface, (255, 255, 255), rect, 2)
                elif tile == T_HOLE:
                    pygame.draw.rect(surface, (50, 0, 0), rect) 
                    pygame.draw.rect(surface, (150, 50, 50), rect, 2)

def create_arena_from_layout(level_str, falling_block_config=None):
    # ubah String Map (T, ., 1, a) menjadi Object Arena
    rows = len(level_str)
    cols = len(level_str[0])
    layout = [[T_AIR for _ in range(cols)] for _ in range(rows)]
    
    start_pos = (1, 1)
    exit_pos = (1, 1)
    hole_positions = {}   
    button_positions = {} 

    for r, row_str in enumerate(level_str):
        for c, char in enumerate(row_str):
            if char == 'T': layout[r][c] = T_GROUND 
            elif char == '.': layout[r][c] = T_AIR
            elif char == 'S': start_pos = (c, r); layout[r][c] = T_AIR
            elif char == 'F': exit_pos = (c, r); layout[r][c] = T_EXIT
            
            # Data Lubang
            elif char in ['1', '2', '3', '4', '5', '7', '8', '9']:
                layout[r][c] = T_HOLE 
                if char not in hole_positions: hole_positions[char] = []
                hole_positions[char].append((c, r))
            
            # Data Tombol
            elif char in ['a', 'b', 'c', 'd', 'e', 'g', 'h', 'i']:
                layout[r][c] = T_BUTTON 
                if char not in button_positions: button_positions[char] = []
                button_positions[char].append((c, r))

    return Arena(layout, rows, cols, start_pos, exit_pos, 
                 hole_positions, button_positions, 
                 falling_block_config)