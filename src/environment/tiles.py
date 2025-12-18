# src/environment/tiles.py
import os
import pygame

TILE_SIZE = 48
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
    # T_EXIT is NOT solid - players can pass through finish tile
    return tile_id in (T_GROUND, T_WALL, T_BUTTON)

def get_tile_color(tile_id: int):
    """Get color fallback untuk tile types"""
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


# Tile sprite manager
class TileSpriteManager:
    """Manages loading and rendering of 9 tile types from PNG sprites"""
    
    def __init__(self):
        self.tiles_dir = os.path.join(
            os.path.dirname(os.path.dirname(os.path.dirname(__file__))),
            "assets", "images", "tiles"
        )
        self.sprites = {}
        self._load_all_tiles()
    
    def _load_all_tiles(self):
        """Load all 9 tile types"""
        tile_names = [
            'tiles_bottom',
            'tiles_bottom_left',
            'tiles_bottom_right',
            'tiles_center',
            'tiles_left',
            'tiles_right',
            'tiles_top_center',
            'tiles_top_left',
            'tiles_top_right'
        ]
        
        for name in tile_names:
            self._load_tile(name)
    
    def _load_tile(self, name):
        """Load single tile sprite"""
        filepath = os.path.join(self.tiles_dir, f"{name}.png")
        try:
            img = pygame.image.load(filepath).convert_alpha()
            # Scale to TILE_SIZE
            self.sprites[name] = pygame.transform.scale(img, (TILE_SIZE, TILE_SIZE))
        except Exception as e:
            print(f"Warning: failed to load tile sprite '{name}': {e}")
            self.sprites[name] = None
    
    def get_tile_sprite(self, tile_type: int, col: int, row: int, grid: list = None):
        """
        Get appropriate sprite tile berdasarkan positioning rules:
        
        Walkable tiles (top_*): Use when this is the top surface players can stand on
        Non-walkable tiles: Use for walls, base, and internal structure
        
        Parameters:
        - tile_type: T_GROUND, T_WALL, T_BUTTON, etc.
        - col, row: Position dalam grid
        - grid: Arena layout untuk check surrounding tiles
        
        Returns sprite surface atau None
        """
        if tile_type != T_GROUND and tile_type != T_WALL:
            return None
        
        # Jika grid tidak provided, gunakan center sprite
        if grid is None:
            return self.sprites.get('tiles_center')
        
        rows = len(grid)
        cols = len(grid[0]) if rows > 0 else 0
        
        # Check if there is air/hole above this tile (makes it a walkable surface)
        is_top_surface = False
        if row > 0:
            tile_above = grid[row - 1][col]
            # Tile is walkable surface if there's air or hole above
            is_top_surface = (tile_above == T_AIR or tile_above == T_HOLE)
        elif row == 0:
            # Top edge always has air above
            is_top_surface = True
        
        # Edge detection
        is_left_edge = col == 0
        is_right_edge = col == cols - 1
        is_bottom_edge = row == rows - 1
        
        # WALKABLE TILES: Only use tiles_top_* if this is a top surface
        if is_top_surface:
            if is_left_edge:
                return self.sprites.get('tiles_top_left')
            elif is_right_edge:
                return self.sprites.get('tiles_top_right')
            else:
                return self.sprites.get('tiles_top_center')
        
        # NON-WALKABLE TILES: Choose based on position in structure
        # Bottom tiles (base of arena)
        if is_bottom_edge:
            if is_left_edge:
                return self.sprites.get('tiles_bottom_left')
            elif is_right_edge:
                return self.sprites.get('tiles_bottom_right')
            else:
                return self.sprites.get('tiles_bottom')
        
        # Side walls (not on bottom, not walkable top)
        if is_left_edge:
            return self.sprites.get('tiles_left')
        if is_right_edge:
            return self.sprites.get('tiles_right')
        
        # Center/internal tiles (fully surrounded, not on edges)
        return self.sprites.get('tiles_center')
    
    def draw_tile_at(self, surface, x, y, tile_type, col, row, grid=None):
        """Draw tile sprite at screen position"""
        sprite = self.get_tile_sprite(tile_type, col, row, grid)
        if sprite:
            surface.blit(sprite, (x, y))
        else:
            # Fallback jika sprite tidak ada
            color = get_tile_color(tile_type)
            if color:
                pygame.draw.rect(surface, color, (x, y, TILE_SIZE, TILE_SIZE))


# Global instance
_tile_sprite_manager = None


def get_tile_sprite_manager():
    """Get or create global tile sprite manager"""
    global _tile_sprite_manager
    if _tile_sprite_manager is None:
        _tile_sprite_manager = TileSpriteManager()
    return _tile_sprite_manager