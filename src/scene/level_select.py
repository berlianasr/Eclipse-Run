import os
import json
import pygame
from .base_screen import BaseScreen
from ..ui.button import Button

BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
IMAGE_DIR = os.path.join(BASE_DIR, "assets", "images", "ui")
MENU_BACKGROUND_IMAGE = "menu_bg.jpeg"
HIGH_SCORES_FILE = os.path.join(BASE_DIR, "assets", "data", "high_scores.json")

NEON_PURPLE_FILL = (90, 40, 140)    # Isian ungu bagian dalam
NEON_PINK_BORDER = (255, 100, 255) # Garis tepi tebal
BACK_BUTTON_COLOR = (255, 50, 100)  # Pink/Merah untuk tombol BACK
BACK_BUTTON_TEXT_COLOR = (255, 255, 255)
BORDER_THICKNESS = 8
LEVEL_BOX_SIZE = 120  # membuat kotak lebih kecil
LEVEL_IMAGE_DISPLAY_SIZE = (140, 140)  # ukuran awal saat memuat (dipakai sebagai fallback)
LEVEL_NUMBER_RENDER_SIZE = (220, 220) 
LOCK_IMAGE_SIZE = (72, 72)
MAX_UPSCALE = 2.5 

class LevelSelectScreen(BaseScreen):
    def __init__(self, manager, screen_width, screen_height):
        super().__init__(manager, screen_width, screen_height)

        #LOAD BACKGROUND
        background_path = os.path.join(IMAGE_DIR, MENU_BACKGROUND_IMAGE)
        try:
            original_image = pygame.image.load(background_path).convert() 
            self.background_image = pygame.transform.scale(
                original_image, (screen_width, screen_height)
            )
        except Exception as e:
            print(f"Error loading background image: {e}. Using solid color fallback.")
            self.background_image = None 

        self.button_font = pygame.font.SysFont(None, 36)

        # Check unlocked levels berdasarkan high scores
        self.unlocked_level = self._get_unlocked_level() 

        # Load UI Images
        self.level_images = {}
        self.lock_image = None
        self.level_text_image = None
        self._load_ui_images()

        #INISIALISASI TOMBOL LEVEL
        self.level_buttons = []

        spacing = 50
        start_x = (screen_width - (3 * LEVEL_BOX_SIZE + 2 * spacing)) // 2
        y = screen_height // 2 - 50 

        for i in range(1, 4):
            unlocked = i <= self.unlocked_level

            rect = pygame.Rect(
                start_x + (i - 1) * (LEVEL_BOX_SIZE + spacing),
                y,
                LEVEL_BOX_SIZE,
                LEVEL_BOX_SIZE
            )

            btn = Button(
                rect,
                f"{i}",
                self.button_font,
                bg_color=NEON_PURPLE_FILL 
            )

            btn.level = i
            btn.unlocked = unlocked
            btn.border_radius = 20
            self.level_buttons.append(btn)

        #INISIALISASI TOMBOL BACK
        back_button_rect = pygame.Rect(30, 30, 120, 50) 
        self.back_button = Button(
            back_button_rect,
            "BACK",
            self.button_font,
            bg_color=BACK_BUTTON_COLOR,
            text_color=BACK_BUTTON_TEXT_COLOR
        )
        self.back_button.border_radius = 5

    def _get_unlocked_level(self):
        """Check high scores file untuk determine unlocked levels.
        Level 1 selalu unlocked.
        Level 2 unlock jika level 1 sudah ada score.
        Level 3 unlock jika level 2 sudah ada score.
        """
        try:
            if os.path.exists(HIGH_SCORES_FILE):
                with open(HIGH_SCORES_FILE, 'r') as f:
                    scores_data = json.load(f)
                    
                    # Check level 2
                    if scores_data.get('level_2') and len(scores_data['level_2']) > 0:
                        # Level 3 unlock jika level 2 sudah ada score
                        return 3
                    
                    # Check level 1
                    if scores_data.get('level_1') and len(scores_data['level_1']) > 0:
                        # Level 2 unlock jika level 1 sudah ada score
                        return 2
        except Exception as e:
            print(f"Error checking unlocked levels: {e}")
        
        # Default: hanya level 1 yang unlocked
        return 1

    def _load_ui_images(self):
        """Load semua gambar UI yang diperlukan, dengan penskalaan ke ukuran tampilan."""
        # Load gambar angka level 1, 2, 3
        for i in range(1, 4):
            image_path = os.path.join(IMAGE_DIR, f"{i}.png")
            try:
                img = pygame.image.load(image_path).convert_alpha()
                # Keep original so we can render it larger than the box if desired
                if not hasattr(self, 'level_images_orig'):
                    self.level_images_orig = {}
                self.level_images_orig[i] = img
                # Skala gambar ke ukuran target sambil menjaga aspek rasio (fallback)
                self.level_images[i] = self._scale_preserve(img, LEVEL_IMAGE_DISPLAY_SIZE)
            except Exception as e:
                print(f"Error loading level {i} image: {e}")
                self.level_images[i] = None

        # Load gambar lock (gembok)
        lock_path = os.path.join(IMAGE_DIR, "lock.png")
        try:
            img = pygame.image.load(lock_path).convert_alpha()
            self.lock_image = self._scale_preserve(img, LOCK_IMAGE_SIZE)
        except Exception as e:
            print(f"Error loading lock image: {e}")
            self.lock_image = None

        # Load gambar "level" text (judul)
        level_text_path = os.path.join(IMAGE_DIR, "level.png")
        try:
            img = pygame.image.load(level_text_path).convert_alpha()
            self.level_text_image_orig = img
            self.level_text_image = None
        except Exception as e:
            print(f"Error loading level text image: {e}")
            self.level_text_image_orig = None
            self.level_text_image = None

    def _scale_preserve(self, image: pygame.Surface, max_size: tuple) -> pygame.Surface:
        """Scale surface preserving aspect ratio to fit inside max_size.

        Args:
            image: source surface
            max_size: (max_width, max_height)

        Returns:
            A new scaled Surface (or the original if no scaling needed).
        """
        w, h = image.get_size()
        max_w, max_h = max_size
        scale = min(max_w / w, max_h / h)
        if scale > MAX_UPSCALE:
            scale = MAX_UPSCALE

        target_w, target_h = max(1, int(w * scale)), max(1, int(h * scale))
        try:
            return pygame.transform.smoothscale(image, (target_w, target_h))
        except Exception:
            return pygame.transform.scale(image, (target_w, target_h))

    def handle_event(self, event):
        if self.back_button.handle_event(event):
            try:
                from .main_menu import MainMenuScreen
                main_menu = MainMenuScreen(self.manager, self.screen_width, self.screen_height)
                self.manager.switch_to(main_menu)
                return
            except ImportError:
                print("Error: Could not import MainMenuScreen. Falling back to string switch.")
                self.manager.switch_to('main_menu')
                return

        for btn in self.level_buttons:
            if not btn.unlocked:
                continue

            if btn.handle_event(event):
                self.start_level(btn.level)

    def start_level(self, level):
        if level == 1:
            from .level1 import Level1
            next_screen = Level1(self.manager, self.screen_width, self.screen_height)
        elif level == 2:
            from .level2 import Level2
            next_screen = Level2(self.manager, self.screen_width, self.screen_height)
        elif level == 3:
            from .level3 import Level3
            next_screen = Level3(self.manager, self.screen_width, self.screen_height)
        else:
            return

        self.manager.switch_to(next_screen)

    def draw(self, surface):
        # Draw background
        if self.background_image:
            surface.blit(self.background_image, (0, 0))
        else:
            surface.fill((20, 20, 30))

        if hasattr(self, 'level_text_image_orig') and self.level_text_image_orig:
            max_w = int(self.screen_width * 0.95)
            max_h = int(self.screen_height * 0.5)
            scaled_title = self._scale_preserve(self.level_text_image_orig, (max_w, max_h))
            text_x = (self.screen_width - scaled_title.get_width()) // 2
            if self.level_buttons:
                boxes_top = min(b.rect.top for b in self.level_buttons)
                text_y = boxes_top - scaled_title.get_height() + 8
                # ensure not off-screen at top
                if text_y < 8:
                    text_y = 8
            else:
                text_y = 30
            surface.blit(scaled_title, (text_x, text_y))

        #Draw level boxes
        mouse_pos = pygame.mouse.get_pos()
        for i, btn in enumerate(self.level_buttons):

            pygame.draw.rect(surface, NEON_PINK_BORDER, btn.rect, border_radius=btn.border_radius)

            inner_rect = btn.rect.inflate(-BORDER_THICKNESS, -BORDER_THICKNESS)
            inner_radius = btn.border_radius - (BORDER_THICKNESS // 2)
            inner_radius = max(0, inner_radius)

            hovered = btn.rect.collidepoint(mouse_pos)
            if hovered:
                fill_color = tuple(max(0, int(c * 0.55)) for c in NEON_PURPLE_FILL)
            else:
                fill_color = NEON_PURPLE_FILL

            pygame.draw.rect(surface, fill_color, inner_rect, border_radius=inner_radius)

            if hasattr(self, 'level_images_orig') and i + 1 in self.level_images_orig and self.level_images_orig[i + 1]:
                render_img = self._scale_preserve(self.level_images_orig[i + 1], LEVEL_NUMBER_RENDER_SIZE)
                img_x = btn.rect.centerx - render_img.get_width() // 2
                img_y = btn.rect.centery - render_img.get_height() // 2
                surface.blit(render_img, (img_x, img_y))
            elif i + 1 in self.level_images and self.level_images[i + 1]:
                level_img = self.level_images[i + 1]
                img_x = btn.rect.centerx - level_img.get_width() // 2
                img_y = btn.rect.centery - level_img.get_height() // 2
                surface.blit(level_img, (img_x, img_y))

            if not btn.unlocked:
                # 1. Redupkan angka level dengan lapisan transparan
                s = pygame.Surface(btn.rect.size, pygame.SRCALPHA)
                s.fill((0, 0, 0, 120))
                surface.blit(s, btn.rect.topleft)

                if self.lock_image:
                    lock_img = self.lock_image
                    lock_x = btn.rect.centerx - lock_img.get_width() // 2
                    lock_y = btn.rect.centery - lock_img.get_height() // 2
                    surface.blit(lock_img, (lock_x, lock_y))
        
        #Back Button
        self.back_button.draw(surface)

    def update(self, dt: float):
        pass