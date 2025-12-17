import pygame

class PlayerBase:
    def __init__(self, x, y, color):
        self.x = x
        self.y = y
        self.w = 20
        self.h = 20
        self.color = color
        self.speed = 3

    def get_rect(self) -> pygame.Rect:
        return pygame.Rect(int(self.x), int(self.y), self.w, self.h)

    def draw_side(self, screen):
        rect = self.get_rect()
        pygame.draw.rect(screen, self.color, rect, border_radius=4)
        pygame.draw.rect(screen, (40, 40, 40), rect, 2, border_radius=4)

    def draw_top(self, screen):
        rect = self.get_rect()
        center_x = rect.centerx
        center_y = rect.centery
        radius = self.w // 2
        pygame.draw.circle(screen, self.color, (center_x, center_y), radius)
        pygame.draw.circle(screen, (40, 40, 40), (center_x, center_y), radius, 2)
        # Indikator arah
        pygame.draw.line(screen, (40, 40, 40), (center_x, center_y), (center_x, center_y - radius), 2)