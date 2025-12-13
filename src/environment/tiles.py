# src/environment/tiles.py

TILE_SIZE = 48

T_EMPTY = 0
T_GROUND = 1
T_WALL = 2
T_HOLE = 3
T_EXIT = 4


def is_solid(tile_id: int) -> bool:
    """Tile yang dianggap keras / ditempeli player."""
    return tile_id in (T_GROUND, T_WALL)


def get_tile_color(tile_id: int):
    if tile_id == T_GROUND:
        return (180, 180, 255)   # lantai biru muda
    if tile_id == T_WALL:
        return (120, 120, 200)   # tembok biru tua
    if tile_id == T_HOLE:
        return (50, 50, 80)      # lubang gelap
    if tile_id == T_EXIT:
        return (120, 220, 140)   # exit hijau
    return None
