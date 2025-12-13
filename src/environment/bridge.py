# src/environment/bridge.py

from dataclasses import dataclass
from typing import List

from src.environment.tiles import T_GROUND, T_HOLE


@dataclass
class Bridge:
    """
    Representasi jembatan di atas lubang:
    - row        : baris grid tempat jembatan & lubang
    - hole_cols  : list kolom yang jadi lubang
    - btn_left   : kolom tombol kiri
    - btn_right  : kolom tombol kanan
    - active     : kalau True → lubang diganti lantai (bisa dilewati)
    """
    row: int
    hole_cols: List[int]
    btn_left: int
    btn_right: int
    active: bool = False

    def apply_to_grid(self, grid):
        """Terapkan state jembatan ke grid tiles."""
        for c in self.hole_cols:
            grid[self.row][c] = T_GROUND if self.active else T_HOLE

    def set_active(self, grid, active: bool):
        """Ubah state ON/OFF dan langsung update grid."""
        if self.active == active:
            return
        self.active = active
        self.apply_to_grid(grid)

    def is_button_tile(self, row: int, col: int) -> bool:
        """True kalau tile (row,col) adalah salah satu tombol."""
        return row == self.row and col in (self.btn_left, self.btn_right)
