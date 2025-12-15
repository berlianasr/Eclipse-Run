import os
import pygame
from .level_base import BaseScreen
from ..ui.button import Button

BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
IMAGE_DIR = os.path.join(BASE_DIR, "assets", "images", "ui")
MENU_BACKGROUND_IMAGE = "menu_bg.jpeg"
TITLE_IMAGE_FILE = "judul.PNG" 

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

        # --- LOAD GAMBAR LATAR BELAKANG ---
        background_path = os.path.join(IMAGE_DIR, MENU_BACKGROUND_IMAGE)
        try:
            original_image = pygame.image.load(background_path).convert() 
            self.background_image = pygame.transform.scale(
                original_image, (screen_width, screen_height)
            )
        except Exception as e:
            print(f"Error loading background image: {e}. Using solid color fallback.")
            self.background_image = None 

        # --- LOAD GAMBAR JUDUL (LOGO) ---
        title_logo_path = os.path.join(IMAGE_DIR, TITLE_IMAGE_FILE)
        
        try:
            original_logo = pygame.image.load(title_logo_path).convert_alpha()
            
            # PERHITUNGAN RASIO ASPEK agar tidak gepeng
            original_width = original_logo.get_width()
            original_height = original_logo.get_height()
            
            new_width = TARGET_TITLE_WIDTH
            new_height = int((new_width / original_width) * original_height)
            
            self.title_logo_surface = pygame.transform.scale(
                original_logo, (new_width, new_height)
            )
        except Exception as e:
            print(f"ERROR: Gagal memuat gambar judul '{TITLE_IMAGE_FILE}': {e}.")
            self.title_logo_surface = self._create_text_fallback("Eclipse Run", 64, (255, 255, 255))
        # -----------------------------------

        # Font tombol
        self.button_font = pygame.font.SysFont(None, 32)

        # Posisi tombol (tetap di tengah horizontal)
        button_width = 220
        button_height = 50
        
        center_x = screen_width // 2 
        
        # NAIKKAN TOMBOL: Ubah offset Y menjadi -30 (sebelumnya 20)
        BUTTON_OFFSET_Y = -20
        start_y = screen_height // 2 + BUTTON_OFFSET_Y


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

    def _create_text_fallback(self, text, size, color):
        font = pygame.font.SysFont(None, size)
        return font.render(text, True, color)

    def handle_event(self, event: pygame.event.Event):
        if self.start_button.handle_event(event):
            from .level_select import LevelSelectScreen
            new_screen = LevelSelectScreen(self.manager, self.screen_width, self.screen_height)
            self.manager.switch_to(new_screen)

        if self.quit_button.handle_event(event):
            pygame.event.post(pygame.event.Event(pygame.QUIT))

    def update(self, dt: float):
        pass

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

        # 3. Gambar Tombol
        self.start_button.draw(surface)
        self.highscore_button.draw(surface)
        self.quit_button.draw(surface)