# src/systems/pov.py
from enum import Enum


class POVMode(Enum):
    SIDE = "side"  # Gravitasi ke bawah, jalan di tanah
    TOP = "top"    # Gravitasi ke belakang, jalan di tembok


class POVController:
    def __init__(self):
        self.mode = POVMode.SIDE
    
    def toggle(self):
        # Toggle antara SIDE dan TOP mode
        if self.mode == POVMode.SIDE:
            self.mode = POVMode.TOP
        else:
            self.mode = POVMode.SIDE
    
    def is_side(self) -> bool:
        # Return True jika mode SIDE (normal)
        return self.mode == POVMode.SIDE
    
    def is_top(self) -> bool:
        #Return True jika mode TOP (tembok)
        return self.mode == POVMode.TOP
    
    def get_mode(self) -> POVMode:
        return self.mode