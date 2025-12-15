import abc
import pygame


class BaseScreen(abc.ABC):
    def __init__(self, manager, screen_width: int, screen_height: int):
        self.manager = manager
        self.screen_width = screen_width
        self.screen_height = screen_height

    @abc.abstractmethod
    def handle_event(self, event: pygame.event.Event):
        ...

    @abc.abstractmethod
    def update(self, dt: float):
        ...

    @abc.abstractmethod
    def draw(self, surface: pygame.Surface):
        ...
