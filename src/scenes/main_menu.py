import os
import pygame
from .level_base import BaseScreen
from ..ui.button import Button

BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
IMAGE_DIR = os.path.join(BASE_DIR, "assets", "images", "ui")
CHARACTERS_DIR = os.path.join(BASE_DIR, "assets", "images")
MENU_BACKGROUND_IMAGE = "menu_bg.jpeg"
TITLE_IMAGE_FILE = "judul.PNG"
SUN_WALK_A = os.path.join(CHARACTERS_DIR, "sun", "character_yellow_walk_a.png")
SUN_WALK_B = os.path.join(CHARACTERS_DIR, "sun", "character_yellow_walk_b.png")
MOON_WALK_A = os.path.join(CHARACTERS_DIR, "moon", "character_purple_walk_a.png")
MOON_WALK_B = os.path.join(CHARACTERS_DIR, "moon", "character_purple_walk_b.png") 

TARGET_TITLE_WIDTH = 400 
# NAIKKAN JUDUL: Ubah posisi Y dari 120 menjadi 80
TITLE_Y_POSITION = 70 
# ------------------------------------------------

class MainMenuScreen(BaseScreen):
    def __init__(self, manager, screen_width: int, screen_height: int):
        super().__init__(manager, screen_width, screen_height)

        self.background_image = None
        self.background_color = (10, 50, 40)
        self.title_logo_surface = None

        # =================================================
        # LOAD BACKGROUND
        # =================================================
        background_path = os.path.join(IMAGE_DIR, MENU_BACKGROUND_IMAGE)
        try:
            original_image = pygame.image.load(background_path).convert()
            self.background_image = pygame.transform.scale(
                original_image, (screen_width, screen_height)
            )
        except Exception as e:
            print(f"Error loading background image: {e}. Using solid color fallback.")
            self.background_image = None

        # =================================================
        # LOAD TITLE LOGO
        # =================================================
        title_logo_path = os.path.join(IMAGE_DIR, TITLE_IMAGE_FILE)
        try:
            original_logo = pygame.image.load(title_logo_path).convert_alpha()
            original_width = original_logo.get_width()
            original_height = original_logo.get_height()

            new_width = TARGET_TITLE_WIDTH
            new_height = int((new_width / original_width) * original_height)

            self.title_logo_surface = pygame.transform.scale(
                original_logo, (new_width, new_height)
            )
        except Exception as e:
            print(f"ERROR: Gagal memuat gambar judul '{TITLE_IMAGE_FILE}': {e}.")
            self.title_logo_surface = self._create_text_fallback(
                "Eclipse Run", 64, (255, 255, 255)
            )

        # =================================================
        # LOAD CHARACTER SPRITES
        # =================================================
        self.sun_walk_a = None
        self.sun_walk_b = None
        self.moon_walk_a = None
        self.moon_walk_b = None
        self.animation_frame = 0
        self.animation_timer = 0.0
        self.animation_speed = 0.3  # seconds per frame

        # Load sun character sprites
        try:
            self.sun_walk_a = pygame.image.load(SUN_WALK_A).convert_alpha()
            self.sun_walk_b = pygame.image.load(SUN_WALK_B).convert_alpha()
        except Exception as e:
            print(f"Warning: failed to load sun sprites: {e}")

        # Load moon character sprites
        try:
            self.moon_walk_a = pygame.image.load(MOON_WALK_A).convert_alpha()
            self.moon_walk_b = pygame.image.load(MOON_WALK_B).convert_alpha()
        except Exception as e:
            print(f"Warning: failed to load moon sprites: {e}")

        # =================================================
        # FONT
        # =================================================
        self.button_font = pygame.font.SysFont(None, 32)

        # =================================================
        # HITUNG LAYOUT TOMBOL (WAJIB DULU)
        # =================================================
        button_width = 220
        button_height = 50

        center_x = screen_width // 2
        BUTTON_OFFSET_Y = -20
        start_y = screen_height // 2 + BUTTON_OFFSET_Y

        # =================================================
        # TOMBOL-TOMBOL
        # =================================================
        self.start_button = Button(
            pygame.Rect(center_x - button_width // 2, start_y, button_width, button_height),
            "Start Game",
            self.button_font,
        )

        self.highscore_button = Button(
            pygame.Rect(center_x - button_width // 2, start_y + 70, button_width, button_height),
            "High Score",
            self.button_font,
        )

        self.quit_button = Button(
            pygame.Rect(center_x - button_width // 2, start_y + 140, button_width, button_height),
            "Quit",
            self.button_font,
        )

        # =================================================
        # DEBUG BUTTON (PALING BAWAH)
        # =================================================
        self.gameover_button = Button(
            pygame.Rect(center_x - button_width // 2, start_y + 210, button_width, button_height),
            "Game Over (Debug)",
            self.button_font,
        )

    def _create_text_fallback(self, text, size, color):
        font = pygame.font.SysFont(None, size)
        return font.render(text, True, color)

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

    def handle_event(self, event: pygame.event.Event):
        if self.start_button.handle_event(event):
            from .level_select import LevelSelectScreen
            new_screen = LevelSelectScreen(self.manager, self.screen_width, self.screen_height)
            self.manager.switch_to(new_screen)

        if self.quit_button.handle_event(event):
            pygame.event.post(pygame.event.Event(pygame.QUIT))

        if self.gameover_button.handle_event(event):
            from .game_over import GameOverScreen
            self.manager.switch_to(
                GameOverScreen(
                    self.manager,
                    self.screen_width,
                    self.screen_height,
                    score=999  # dummy
                )
            )


    def update(self, dt: float):
        # Update animation timer
        self.animation_timer += dt
        if self.animation_timer >= self.animation_speed:
            self.animation_timer = 0.0
            self.animation_frame = 1 - self.animation_frame  # Toggle between 0 and 1

    def draw(self, surface: pygame.Surface):
        # 1. Gambar Background
        if self.background_image:
            surface.blit(self.background_image, (0, 0))
        else:
            surface.fill(self.background_color)

        # 2. Gambar Judul (Gambar Logo)
        if self.title_logo_surface:
            # Posisi y dihitung berdasarkan TITLE_Y_POSITION = 80
            title_rect = self.title_logo_surface.get_rect(
                center=(self.screen_width // 2, TITLE_Y_POSITION + self.title_logo_surface.get_height() // 2)
            )
            surface.blit(self.title_logo_surface, title_rect)

        # 3. Hitung ukuran karakter berdasarkan tinggi tombol (sedikit lebih besar)
        button_top = self.start_button.rect.top
        button_bottom = self.quit_button.rect.bottom
        character_height = button_bottom - button_top
        character_size = int(character_height * 1.15)  # 15% lebih besar
        
        # 4. Gambar karakter sun di kiri (samping tombol)
        if self.sun_walk_a and self.sun_walk_b:
            sun_sprite = self.sun_walk_a if self.animation_frame == 0 else self.sun_walk_b
            sun_scaled = self._scale_preserve(sun_sprite, (character_size, character_size))
            sun_x = self.start_button.rect.left - sun_scaled.get_width() - 15  # 15px margin dari tombol
            sun_y = button_top - 40 + (character_height - sun_scaled.get_height()) // 2  # naik 20px
            surface.blit(sun_scaled, (sun_x, sun_y))
        
        # 5. Gambar karakter moon di kanan (samping tombol)
        if self.moon_walk_a and self.moon_walk_b:
            moon_sprite = self.moon_walk_a if self.animation_frame == 0 else self.moon_walk_b
            moon_scaled = self._scale_preserve(moon_sprite, (character_size, character_size))
            moon_x = self.start_button.rect.right + 15  # 15px margin dari tombol
            moon_y = button_top - 40 + (character_height - moon_scaled.get_height()) // 2  # naik 20px
            surface.blit(moon_scaled, (moon_x, moon_y))

        # 6. Gambar Tombol
        self.start_button.draw(surface)
        self.highscore_button.draw(surface)
        self.quit_button.draw(surface)
        self.gameover_button.draw(surface)
