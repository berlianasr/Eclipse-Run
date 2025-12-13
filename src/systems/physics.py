# src/systems/physics.py
import pygame
from src.environment.tiles import TILE_SIZE, is_solid, T_EMPTY, T_HOLE


def _get_tile_id(arena, row, col):
    if row < 0 or row >= arena.rows or col < 0 or col >= arena.cols:
        return T_EMPTY
    return arena.layout[row][col]


def _rect_collides_solid(arena, rect: pygame.Rect) -> bool:
    top = (rect.top - arena.origin_y) // TILE_SIZE
    bottom = (rect.bottom - 1 - arena.origin_y) // TILE_SIZE
    left = rect.left // TILE_SIZE
    right = (rect.right - 1) // TILE_SIZE

    for r in range(top, bottom + 1):
        for c in range(left, right + 1):
            tile_id = _get_tile_id(arena, r, c)
            if is_solid(tile_id):
                return True
    return False


def move_with_collisions(player, arena, dx, dy) -> bool:
    """
    Gerakkan player dengan collision terhadap tile solid.
    Return:
        fell_in_hole: True kalau posisi akhir player di atas tile HOLE.
    """
    rect = player.get_rect()

    # Gerak horizontal dulu
    if dx != 0:
        rect.x += dx
        if _rect_collides_solid(arena, rect):
            step = 1 if dx > 0 else -1
            while dx != 0:
                rect.x -= step
                dx -= step
                if not _rect_collides_solid(arena, rect):
                    break

    # Gerak vertikal
    if dy != 0:
        rect.y += dy
        if _rect_collides_solid(arena, rect):
            step = 1 if dy > 0 else -1
            while dy != 0:
                rect.y -= step
                dy -= step
                if not _rect_collides_solid(arena, rect):
                    break

    # Simpan posisi akhir
    player.x = rect.x
    player.y = rect.y

    # Cek tile tepat di bawah kaki (untuk lubang)
    center_x = rect.centerx
    foot_y = rect.bottom - 1
    col = center_x // TILE_SIZE
    row = (foot_y - arena.origin_y) // TILE_SIZE

    tile_id = _get_tile_id(arena, row, col)
    return tile_id == T_HOLE
