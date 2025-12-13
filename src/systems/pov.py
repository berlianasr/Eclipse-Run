# src/systems/pov.py
import enum

class POVMode(enum.Enum):
    SIDE = 0
    TOP = 1

class POVController:
    def __init__(self):
        self.mode = POVMode.SIDE

    def toggle(self):
        self.mode = POVMode.TOP if self.mode == POVMode.SIDE else POVMode.SIDE

    def is_side(self):
        return self.mode == POVMode.SIDE

    def is_top(self):
        return self.mode == POVMode.TOP
