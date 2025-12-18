# src/entities/moon.py
import pygame
from .player_base import PlayerBase

class Moon(PlayerBase):
    def __init__(self, x, y):
        super().__init__(x, y, (150, 140, 250), character_name='moon')  # ungu

    def get_desired_move(self, keys):
        dx = dy = 0
        if keys[pygame.K_a]:
            dx -= self.speed
        if keys[pygame.K_d]:
            dx += self.speed
        if keys[pygame.K_w]:
            dy -= self.speed
        if keys[pygame.K_s]:
            dy += self.speed
        
        # Update facing direction
        self.set_direction(dx)
        
        return dx, dy
