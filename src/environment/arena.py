import pygame
import os
from src.core import settings
from src.environment.tiles import (
    TILE_SIZE, T_GROUND, T_AIR, T_EXIT, T_BUTTON, T_HOLE, T_WALL, T_GATE,
    get_tile_color, get_tile_sprite_manager
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
        
        # Arena background
        self.arena_background = None
        self._load_arena_background()
        
        # Finish sprite states
        self.finish_sprite_closed = None
        self.finish_sprite_open = None
        self.is_finish_open = False  # Updated dari level_base saat kedua players di finish
        
        # Hole sprite
        self.hole_sprite = None
        
        # Switch/button sprites
        self.switch_sprite_normal = None
        self.switch_sprite_pressed = None
        self.pressed_buttons = set()  # Track which buttons are currently pressed (col, row)
        
        self._load_finish_sprites()
        self._load_hole_sprite()
        self._load_switch_sprites()
        
        # Posisi obstacle
        self.hole_positions = hole_positions if hole_positions else {}
        self.button_positions = button_positions if button_positions else {}
        
        # data config balok
        self.falling_block_config = falling_block_config
    
    def _load_arena_background(self):
        """Load arena_bg.jpeg dan darkenkan"""
        base_dir = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
        ui_dir = os.path.join(base_dir, "assets", "images", "ui")
        
        try:
            img = pygame.image.load(os.path.join(ui_dir, "arena_bg.jpeg")).convert()
            # Scale to screen size
            self.arena_background = pygame.transform.scale(img, (settings.WIDTH, settings.HEIGHT))
            
            # Darken the background dengan overlay
            darkness = pygame.Surface((settings.WIDTH, settings.HEIGHT))
            darkness.fill((0, 0, 0))
            darkness.set_alpha(80)  # 80 alpha untuk darkening
            self.arena_background.blit(darkness, (0, 0))
        except Exception as e:
            print(f"Warning: failed to load arena background: {e}")
    
    def _load_hole_sprite(self):
        """Load block_red.png sprite untuk hole"""
        base_dir = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
        obstacle_dir = os.path.join(base_dir, "assets", "images", "obstacle")
        
        try:
            img = pygame.image.load(os.path.join(obstacle_dir, "block_red.png")).convert_alpha()
            self.hole_sprite = pygame.transform.scale(img, (TILE_SIZE, TILE_SIZE))
        except Exception as e:
            print(f"Warning: failed to load hole sprite (block_red.png): {e}")
    
    def _load_switch_sprites(self):
        """Load switch_red.png dan switch_red_pressed.png sprites"""
        base_dir = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
        tiles_dir = os.path.join(base_dir, "assets", "images", "tiles")
        
        # Load switch_red.png
        try:
            img = pygame.image.load(os.path.join(tiles_dir, "switch_red.png")).convert_alpha()
            self.switch_sprite_normal = pygame.transform.scale(img, (TILE_SIZE, TILE_SIZE))
        except Exception as e:
            print(f"Warning: failed to load switch_red.png: {e}")
        
        # Load switch_red_pressed.png
        try:
            img = pygame.image.load(os.path.join(tiles_dir, "switch_red_pressed.png")).convert_alpha()
            self.switch_sprite_pressed = pygame.transform.scale(img, (TILE_SIZE, TILE_SIZE))
        except Exception as e:
            print(f"Warning: failed to load switch_red_pressed.png: {e}")
    
    def _load_finish_sprites(self):
        """Load finish.png dan finish_open.png sprites - enlarged untuk lebih terlihat"""
        base_dir = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
        tiles_dir = os.path.join(base_dir, "assets", "images", "tiles")
        
        # Enlarged size untuk finish door (2x TILE_SIZE)
        finish_size = TILE_SIZE
        
        # Load finish.png
        try:
            img = pygame.image.load(os.path.join(tiles_dir, "finish.png")).convert_alpha()
            self.finish_sprite_closed = pygame.transform.scale(img, (finish_size, finish_size))
        except Exception as e:
            print(f"Warning: failed to load finish.png: {e}")
        
        # Load finish_open.png
        try:
            img = pygame.image.load(os.path.join(tiles_dir, "finish_open.png")).convert_alpha()
            self.finish_sprite_open = pygame.transform.scale(img, (finish_size, finish_size))
        except Exception as e:
            print(f"Warning: failed to load finish_open.png: {e}") 

    def draw_side(self, surface):
        # Draw arena background terlebih dahulu
        if self.arena_background:
            surface.blit(self.arena_background, (0, 0))
        
        self._draw_grid(surface, is_side=True)
        self._draw_switches(surface, is_side=True)

    def draw_top(self, surface):
        # Draw arena background terlebih dahulu
        if self.arena_background:
            surface.blit(self.arena_background, (0, 0))
        
        self._draw_grid(surface, is_side=False)
        self._draw_switches(surface, is_side=False)  # Show switches even in TOP POV
    
    def _draw_switches(self, surface, is_side=True):
        """Draw switch sprites di atas button tiles (visible in both POV, only pressable in SIDE)"""
        for button_id, positions in self.button_positions.items():
            for col, row in positions:
                x = col * TILE_SIZE
                y = row * TILE_SIZE
                
                # Check jika button sedang ditekan (only in SIDE POV)
                is_pressed = is_side and ((col, row) in self.pressed_buttons)
                
                if is_pressed and self.switch_sprite_pressed:
                    surface.blit(self.switch_sprite_pressed, (x, y))
                elif self.switch_sprite_normal:
                    surface.blit(self.switch_sprite_normal, (x, y))

    def _draw_grid(self, surface, is_side=True):
        """Draw grid using tile sprites with fallback to color rects"""
        tile_manager = get_tile_sprite_manager()
        
        for r in range(self.rows):
            for c in range(self.cols):
                tile = self.layout[r][c]
                x = c * TILE_SIZE
                y = r * TILE_SIZE
                rect = pygame.Rect(x, y, TILE_SIZE, TILE_SIZE)
                
                if tile == T_GROUND or tile == T_WALL:
                    # Use tile sprite dengan fallback to color
                    tile_manager.draw_tile_at(surface, x, y, tile, c, r, self.layout)
                elif tile == T_EXIT:
                    # Render finish sprite (closed atau open) - 1x TILE_SIZE
                    if c == self.exit_pos[0] and r == self.exit_pos[1]:
                        finish_x = x
                        finish_y = y
                        
                        if self.is_finish_open and self.finish_sprite_open:
                            surface.blit(self.finish_sprite_open, (finish_x, finish_y))
                        elif self.finish_sprite_closed:
                            surface.blit(self.finish_sprite_closed, (finish_x, finish_y))
                        else:
                            pygame.draw.rect(surface, (0, 255, 0), rect)
                    else:
                        pygame.draw.rect(surface, (0, 255, 0), rect)

                elif tile == T_BUTTON:
                    pygame.draw.rect(surface, (0, 200, 200), rect)
                    pygame.draw.rect(surface, (255, 255, 255), rect, 2)
                elif tile == T_HOLE:
                    # Render hole sprite (block_red.png)
                    if self.hole_sprite:
                        surface.blit(self.hole_sprite, (x, y))
                    else:
                        # Fallback drawing
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