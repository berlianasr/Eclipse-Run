import pygame


class ScreenManager:
    def __init__(self, initial_screen):
        # initial_screen adalah instance dari screen pertama (misal MainMenuScreen)
        self.current_screen = initial_screen

    def switch_to(self, new_screen):
        self.current_screen = new_screen

    def handle_event(self, event: pygame.event.Event):
        if self.current_screen is not None:
            self.current_screen.handle_event(event)

    def update(self, dt: float):
        if self.current_screen is not None:
            self.current_screen.update(dt)

    def draw(self, surface: pygame.Surface):
        if self.current_screen is not None:
            self.current_screen.draw(surface)
