import os
import pygame
from .level_base import BaseScreen
from ..ui.button import Button

# Image directory (project root -> assets/images/ui)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
IMAGE_DIR = os.path.join(BASE_DIR, "assets", "images", "ui")
MENU_BACKGROUND_IMAGE = "menu_bg.jpeg"
OVER_IMAGE = "over.png"


class GameOverScreen(BaseScreen):
    def __init__(self, manager, screen_width, screen_height, score=0):
        super().__init__(manager, screen_width, screen_height)

        self.score = score

        # Try to load background image; fallback to solid color
        self.background_color = (20, 20, 20)
        bg_path = os.path.join(IMAGE_DIR, MENU_BACKGROUND_IMAGE)
        try:
            bg = pygame.image.load(bg_path).convert_alpha()
            self.background_image = pygame.transform.smoothscale(bg, (self.screen_width, self.screen_height))
        except Exception as e:
            print(f"Warning: failed to load game over background '{bg_path}': {e}")
            self.background_image = None

        # Font
        self.score_font = pygame.font.SysFont(None, 36)
        self.button_font = pygame.font.SysFont(None, 32)

        # Load "GAME OVER" image
        self.over_image_orig = None
        self.over_image = None
        over_path = os.path.join(IMAGE_DIR, OVER_IMAGE)
        try:
            img = pygame.image.load(over_path).convert_alpha()
            self.over_image_orig = img
            # Scale to larger size (max width 90% of screen, height 35% of screen)
            max_w = int(self.screen_width * 0.9)
            max_h = int(self.screen_height * 0.35)
            self.over_image = self._scale_preserve(img, (max_w, max_h))
        except Exception as e:
            print(f"Warning: failed to load over image '{over_path}': {e}")

        # Score text surface
        self.score_surface = self.score_font.render(
            f"Score: {self.score}", True, (255, 255, 255)
        )

        # Button layout
        button_width = 220
        button_height = 50
        center_x = screen_width // 2
        start_y = screen_height // 2 + 60

        self.retry_button = Button(
            pygame.Rect(center_x - button_width // 2, start_y, button_width, button_height),
            "Retry",
            self.button_font
        )

        self.menu_button = Button(
            pygame.Rect(center_x - button_width // 2, start_y + 70, button_width, button_height),
            "Back to Menu",
            self.button_font
        )

    # =====================================================
    # REQUIRED ABSTRACT METHODS
    # =====================================================
    def handle_event(self, event: pygame.event.Event):
        if self.retry_button.handle_event(event):
            # Placeholder: nanti bisa diganti retry level terakhir
            from .main_menu import MainMenuScreen
            self.manager.switch_to(
                MainMenuScreen(self.manager, self.screen_width, self.screen_height)
            )

        if self.menu_button.handle_event(event):
            from .main_menu import MainMenuScreen
            self.manager.switch_to(
                MainMenuScreen(self.manager, self.screen_width, self.screen_height)
            )

    def update(self, dt: float):
        # Tidak ada animasi dulu → aman
        pass

    def _scale_preserve(self, image: pygame.Surface, max_size: tuple) -> pygame.Surface:
        """Scale surface preserving aspect ratio to fit inside max_size."""
        w, h = image.get_size()
        max_w, max_h = max_size
        scale = min(max_w / w, max_h / h)
        target_w, target_h = max(1, int(w * scale)), max(1, int(h * scale))
        try:
            return pygame.transform.smoothscale(image, (target_w, target_h))
        except Exception:
            return pygame.transform.scale(image, (target_w, target_h))

    def draw(self, surface: pygame.Surface):
        # Draw background image (darkened) or fallback color
        if getattr(self, 'background_image', None):
            surface.blit(self.background_image, (0, 0))
            # overlay semi-transparent black to darken slightly
            overlay = pygame.Surface((self.screen_width, self.screen_height), pygame.SRCALPHA)
            overlay.fill((0, 0, 0, 90))  # alpha ~90/255
            surface.blit(overlay, (0, 0))
        else:
            surface.fill(self.background_color)

        # Draw "GAME OVER" image
        if self.over_image:
            over_rect = self.over_image.get_rect(
                center=(self.screen_width // 2, self.screen_height // 2 - 80)
            )
            surface.blit(self.over_image, over_rect)

        # Score (lowered position)
        score_rect = self.score_surface.get_rect(
            center=(self.screen_width // 2, self.screen_height // 2 + 40)
        )
        surface.blit(self.score_surface, score_rect)

        # Buttons
        self.retry_button.draw(surface)
        self.menu_button.draw(surface)
