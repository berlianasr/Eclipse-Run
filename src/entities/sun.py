# src/entities/sun.py
import pygame
from .player_base import PlayerBase

class Sun(PlayerBase):
    def __init__(self, x, y):
        super().__init__(x, y, (255, 210, 60), character_name='sun')  # kuning

    def get_desired_move(self, keys):
        dx = dy = 0
        if keys[pygame.K_LEFT]:
            dx -= self.speed
        if keys[pygame.K_RIGHT]:
            dx += self.speed
        if keys[pygame.K_UP]:
            dy -= self.speed
        if keys[pygame.K_DOWN]:
            dy += self.speed
        
        # Update facing direction
        self.set_direction(dx)
        
        return dx, dy
