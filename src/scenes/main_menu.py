import os
import pygame
from .level_base import BaseScreen
from ..ui.button import Button

BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
IMAGE_DIR = os.path.join(BASE_DIR, "assets", "images", "ui")
MENU_BACKGROUND_IMAGE = "menu_bg.jpeg"

class MainMenuScreen(BaseScreen):
    def __init__(self, manager, screen_width: int, screen_height: int):
        super().__init__(manager, screen_width, screen_height)

        self.background_image = None
        self.background_color = (10, 50, 40) # Warna fallback jika gambar gagal dimuat

        background_path = os.path.join(IMAGE_DIR, MENU_BACKGROUND_IMAGE)
        
        try:
            # MEMUAT GAMBAR
            # Gunakan .convert() untuk optimasi
            original_image = pygame.image.load(background_path).convert() 
            
            # Skalakan agar sesuai dengan ukuran layar
            self.background_image = pygame.transform.scale(
                original_image, (screen_width, screen_height)
            )
            print(f"Background image '{MENU_BACKGROUND_IMAGE}' loaded successfully.")
        except (pygame.error, FileNotFoundError) as e:
            # Tambahkan logika fallback jika ada error loading gambar
            print(f"Error loading background image from {background_path}: {e}. Using solid color fallback.")
            self.background_image = None # Pastikan ini None jika gagal dimuat

        self.title_font = pygame.font.SysFont(None, 64)
        self.button_font = pygame.font.SysFont(None, 32)

        # Posisi tombol
        button_width = 220
        button_height = 50
        center_x = screen_width // 2
        start_y = screen_height // 2 - 40

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

    def handle_event(self, event: pygame.event.Event):
        if self.start_button.handle_event(event):
            from .game_screen import GameScreen
            new_screen = GameScreen(self.manager, self.screen_width, self.screen_height)
            self.manager.switch_to(new_screen)

        # if self.highscore_button.handle_event(event):
        #     from .high_score import HighScoreScreen
        #     new_screen = HighScoreScreen(self.manager, self.screen_width, self.screen_height)
        #     self.manager.switch_to(new_screen)

        if self.quit_button.handle_event(event):
            pygame.event.post(pygame.event.Event(pygame.QUIT))

    def update(self, dt: float):
        pass

    def draw(self, surface: pygame.Surface):
        # --- PERBAIKAN KRUSIAL DI SINI ---
        if self.background_image:
            # Jika gambar berhasil dimuat (Surface), gunakan BLIT untuk menggambarnya.
            surface.blit(self.background_image, (0, 0))
        else:
            # Jika gambar gagal dimuat, gunakan FILL dengan warna fallback (tuple RGB).
            surface.fill(self.background_color)
        # ---------------------------------

        # Judul
        title_surf = self.title_font.render("Eclipse Run", True, (255, 255, 255))
        title_rect = title_surf.get_rect(center=(self.screen_width // 2, self.screen_height // 2 - 120))
        surface.blit(title_surf, title_rect)

        # Tombol
        self.start_button.draw(surface)
        self.highscore_button.draw(surface)
        self.quit_button.draw(surface)