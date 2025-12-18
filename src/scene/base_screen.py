import pygame


class BaseScreen:
    """Base class untuk semua screen UI (menu, level select, game over)"""
    
    def __init__(self, manager, screen_width: int, screen_height: int):
        self.manager = manager
        self.screen_width = screen_width
        self.screen_height = screen_height
    
    def handle_event(self, event: pygame.event.Event):
        """Handle input events"""
        pass
    
    def update(self, dt: float):
        """Update screen state"""
        pass
    
    def draw(self, surface: pygame.Surface):
        """Draw screen"""
        pass
