import pygame


class Button:
    def __init__(self, rect: pygame.Rect, text: str, font: pygame.font.Font,
                 bg_color=(70, 70, 160), hover_color=(100, 100, 220), text_color=(255, 255, 255)):
        self.rect = rect
        self.text = text
        self.font = font
        self.bg_color = bg_color
        self.hover_color = hover_color
        self.text_color = text_color

    def is_hovered(self, mouse_pos) -> bool:
        return self.rect.collidepoint(mouse_pos)

    def draw(self, surface: pygame.Surface):
        mouse_pos = pygame.mouse.get_pos()
        color = self.hover_color if self.is_hovered(mouse_pos) else self.bg_color

        pygame.draw.rect(surface, color, self.rect, border_radius=8)

        label = self.font.render(self.text, True, self.text_color)
        label_rect = label.get_rect(center=self.rect.center)
        surface.blit(label, label_rect)

    def handle_event(self, event: pygame.event.Event) -> bool:
        """Return True jika tombol diklik (Mouse Left)."""
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.rect.collidepoint(event.pos):
                return True
        return False
