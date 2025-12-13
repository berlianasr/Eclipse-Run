# src/entities/player_base.py
import pygame


class PlayerBase:
    def __init__(self, x, y, color):
        self.x = x
        self.y = y
        self.w = 40
        self.h = 40
        self.color = color
        self.speed = 4

    def get_rect(self) -> pygame.Rect:
        return pygame.Rect(int(self.x), int(self.y), self.w, self.h)

    def draw_side(self, screen):
        rect = self.get_rect()
        pygame.draw.rect(screen, self.color, rect, border_radius=6)
