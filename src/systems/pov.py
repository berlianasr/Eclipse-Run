# src/systems/pov.py
from enum import Enum
from ..audio.sound_manager import get_sound_manager


class POVMode(Enum):
    SIDE = "side"  # Gravitasi ke bawah, jalan di tanah
    TOP = "top"    # Gravitasi ke belakang, jalan di tembok


class POVController:
    def __init__(self):
        self.mode = POVMode.SIDE
        self.sound_manager = get_sound_manager()
    
    def toggle(self):
        """Toggle antara SIDE dan TOP mode dan play sound"""
        if self.mode == POVMode.SIDE:
            self.mode = POVMode.TOP
        else:
            self.mode = POVMode.SIDE
        
        # Play pov change sound
        if self.sound_manager:
            self.sound_manager.play_pov_change()
    
    def is_side(self) -> bool:
        # Return True jika mode SIDE (normal)
        return self.mode == POVMode.SIDE
    
    def is_top(self) -> bool:
        #Return True jika mode TOP (tembok)
        return self.mode == POVMode.TOP
    
    def get_mode(self) -> POVMode:
        return self.mode