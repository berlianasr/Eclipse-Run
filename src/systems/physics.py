# src/systems/physics.py
import pygame
from src.environment.tiles import TILE_SIZE, is_solid, T_HOLE

def move_with_collisions(player, arena, dx, dy, apply_gravity=False, gravity_strength=2):
    # Simpan posisi lama
    old_x = player.x
    old_y = player.y
    
    # Coba gerak horizontal
    player.x += dx
    if _is_colliding(player, arena):
        player.x = old_x  # Kembalikan jika nabrak
    
    # Coba gerak vertikal
    player.y += dy
    if _is_colliding(player, arena):
        player.y = old_y  # Kembalikan jika nabrak
    
    # Terapkan gravitasi (untuk SIDE POV)
    if apply_gravity:
        player.y += gravity_strength
        if _is_colliding(player, arena):
            # Nabrak ground, kembalikan posisi (player berdiri di tanah)
            player.y -= gravity_strength
    
    # Cek apakah player jatuh ke lubang
    if _is_on_hole(player, arena):
        return True  # Player mati
    
    return False  # Aman

def _is_colliding(player, arena) -> bool:
    # Cek apakah player bertabrakan dengan tile solid (tembok/tanah)
    rect = player.get_rect()
    
    # Cek 4 sudut player
    corners = [
        (rect.left, rect.top),
        (rect.right - 1, rect.top),
        (rect.left, rect.bottom - 1),
        (rect.right - 1, rect.bottom - 1),
    ]
    
    for px, py in corners:
        tile_id = _get_tile_at(arena, px, py)
        if tile_id is not None and is_solid(tile_id):
            return True
    
    return False

def _is_on_hole(player, arena) -> bool:
   # Cek apakah player berdiri di atas lubang 
   # Player mati jika centernya ada di lubang dan jembatan tidak aktif
    rect = player.get_rect()
    cx = rect.centerx
    cy = rect.centery
    
    tile_id = _get_tile_at(arena, cx, cy)
    
    if tile_id != T_HOLE:
        return False
    
    # Jika ada jembatan dan aktif, cek apakah player di atas jembatan
    if hasattr(arena, 'bridge') and arena.bridge:
        bridge = arena.bridge
        col = cx // TILE_SIZE
        row = (cy - arena.origin_y) // TILE_SIZE
        
        # Jika player di tile jembatan dan jembatan aktif, aman
        if bridge.active and row == bridge.row and col in bridge.hole_cols:
            return False
    
    # Lubang terbuka, player jatuh
    return True

def _get_tile_at(arena, pixel_x, pixel_y):

    col = pixel_x // TILE_SIZE
    row = (pixel_y - arena.origin_y) // TILE_SIZE
    
    if row < 0 or row >= arena.rows or col < 0 or col >= arena.cols:
        return None
    
    return arena.layout[row][col]

def apply_gravity(player, arena, gravity_strength=0.5):

    # Coba gerakkan ke bawah
    player.y += gravity_strength
    
    # Cek collision
    if _is_colliding(player, arena):
        # Nabrak ground, kembalikan posisi
        player.y -= gravity_strength
        return False
    
    # Cek jatuh ke lubang
    if _is_on_hole(player, arena):
        return True
    
    return False

def check_falling_block_collision(player, rain_blocks) -> bool:
    # Cek apakah player kena balok yang jatuh.

    player_rect = player.get_rect()
    
    for block_rect in rain_blocks.get_active_blocks():
        if player_rect.colliderect(block_rect):
            return True
    
    return False