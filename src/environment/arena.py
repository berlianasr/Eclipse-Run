# src/environment/arena.py
import pygame
from src.core import settings
from src.environment.tiles import (
    TILE_SIZE,
    T_EMPTY,
    T_GROUND,
    T_WALL,
    T_HOLE,
    T_EXIT,
    get_tile_color,
)
from src.environment.bridge import Bridge


class Arena:
    def __init__(self, layout, ground_row_index: int):
        self.layout = layout
        self.rows = len(layout)
        self.cols = len(layout[0]) if self.rows > 0 else 0
        self.ground_row_index = ground_row_index

        total_h = self.rows * TILE_SIZE
        # grid ditempel ke bawah layar
        self.origin_y = settings.HEIGHT - total_h

    def ground_y(self) -> int:
        return self.origin_y + self.ground_row_index * TILE_SIZE

    def draw_side(self, screen: pygame.Surface):
        for r, row in enumerate(self.layout):
            for c, tile_id in enumerate(row):
                color = get_tile_color(tile_id)
                if color is None:
                    continue

                x = c * TILE_SIZE
                y = self.origin_y + r * TILE_SIZE
                rect = pygame.Rect(x, y, TILE_SIZE, TILE_SIZE)

                pygame.draw.rect(screen, color, rect)
                pygame.draw.rect(screen, (40, 40, 40), rect, 1)


def create_level1_arena():
    """
    Level 1:
    - lantai bawah penuh
    - lantai tengah dengan lubang + jembatan + dua tombol
    - lantai atas kiri & kanan
    - exit di lantai atas kanan
    """
    rows = 8
    cols = 20

    grid = [[T_EMPTY for _ in range(cols)] for _ in range(rows)]
    ground_row = rows - 1

    # LANTAI PALING BAWAH
    for c in range(cols):
        grid[ground_row][c] = T_GROUND

    # TEMBOK KECIL DI KIRI & KANAN BAWAH
    grid[ground_row - 1][0] = T_WALL
    grid[ground_row - 1][1] = T_WALL
    grid[ground_row - 1][cols - 2] = T_WALL
    grid[ground_row - 1][cols - 1] = T_WALL

    # PLATFORM TENGAH (di sini ada jembatan dan lubang)
    mid_row = ground_row - 2
    for c in range(3, 15):
        grid[mid_row][c] = T_GROUND

    # Definisi lubang di tengah (dua tile)
    hole_cols = [8, 9]
    for c in hole_cols:
        grid[mid_row][c] = T_HOLE

    # Tombol kiri & kanan (di ujung platform)
    btn_left = 3
    btn_right = 14
    # (tile-nya tetap T_GROUND, kita cuma simpan koordinat tombol di Bridge)

    # PLATFORM ATAS KIRI
    top_row = ground_row - 4
    for c in range(1, 7):
        grid[top_row][c] = T_GROUND

    # PLATFORM ATAS KANAN + EXIT
    for c in range(13, cols - 1):
        grid[top_row][c] = T_GROUND
    grid[top_row][cols - 2] = T_EXIT  # exit hijau

    # Buat objek Bridge (awal: non-aktif / lubang terbuka)
    bridge = Bridge(
        row=mid_row,
        hole_cols=hole_cols,
        btn_left=btn_left,
        btn_right=btn_right,
        active=False,
    )
    bridge.apply_to_grid(grid)

    arena = Arena(grid, ground_row_index=ground_row)
    return arena, bridge
