import os
import json
import pygame
from .base_screen import BaseScreen
from ..ui.button import Button

BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
IMAGE_DIR = os.path.join(BASE_DIR, "assets", "images", "ui")
MENU_BACKGROUND_IMAGE = "menu_bg.jpeg"
HIGH_SCORES_FILE = os.path.join(BASE_DIR, "assets", "data", "high_scores.json")


class HighScoreScreen(BaseScreen):
    def __init__(self, manager, screen_width, screen_height):
        super().__init__(manager, screen_width, screen_height)
        
        self.background_color = (20, 20, 30)
        
        # Load background image
        self.background_image = None
        bg_path = os.path.join(IMAGE_DIR, MENU_BACKGROUND_IMAGE)
        try:
            bg = pygame.image.load(bg_path).convert_alpha()
            self.background_image = pygame.transform.smoothscale(bg, (screen_width, screen_height))
        except Exception as e:
            print(f"Warning: failed to load background '{bg_path}': {e}")
        
        # Load high scores
        self.high_scores = self._load_high_scores()
        
        # Fonts - adjusted sizes for better proportions
        self.title_font = pygame.font.SysFont(None, 56, bold=True)
        self.level_font = pygame.font.SysFont(None, 36)
        self.score_font = pygame.font.SysFont(None, 32)
        self.button_font = pygame.font.SysFont(None, 32)
        
        # Back Button
        button_width = 220
        button_height = 50
        center_x = screen_width // 2
        
        self.back_button = Button(
            pygame.Rect(center_x - button_width // 2, screen_height - 80, button_width, button_height),
            "Back to Menu",
            self.button_font,
            bg_color=(100, 100, 160),
            hover_color=(150, 150, 200)
        )
    
    def _load_high_scores(self):
        """Load high scores dari file JSON"""
        try:
            if os.path.exists(HIGH_SCORES_FILE):
                with open(HIGH_SCORES_FILE, 'r') as f:
                    data = json.load(f)
                    # Format: {"level_1": [{"time": 45.5}, ...], "level_2": [...], "level_3": [...]}
                    return data
        except Exception as e:
            print(f"Error loading high scores: {e}")
        
        return {"level_1": [], "level_2": [], "level_3": []}
    
    def handle_event(self, event: pygame.event.Event):
        if self.back_button.handle_event(event):
            from .main_menu import MainMenuScreen
            self.manager.switch_to(MainMenuScreen(self.manager, self.screen_width, self.screen_height))
    
    def update(self, dt: float):
        pass
    
    def draw(self, surface: pygame.Surface):
        # Draw background
        if self.background_image:
            surface.blit(self.background_image, (0, 0))
            # Overlay semi-transparent dark
            overlay = pygame.Surface((self.screen_width, self.screen_height), pygame.SRCALPHA)
            overlay.fill((0, 0, 0, 100))
            surface.blit(overlay, (0, 0))
        else:
            surface.fill(self.background_color)
        
        # Draw title
        title_surface = self.title_font.render("HIGH SCORES", True, (100, 200, 255))
        title_rect = title_surface.get_rect(center=(self.screen_width // 2, 30))
        surface.blit(title_surface, title_rect)
        
        # Draw high scores untuk setiap level - optimized for screen fit
        y_pos = 90
        level_spacing = 130  
        
        for level_num in range(1, 4):
            level_key = f"level_{level_num}"
            scores = self.high_scores.get(level_key, [])
            
            # Level header
            level_text = self.level_font.render(f"Level {level_num}:", True, (100, 255, 100))
            surface.blit(level_text, (60, y_pos))
            y_pos += 40
            
            # Display top 2 scores (kept in JSON)
            if scores:
                # Sort by time (ascending - semakin cepat semakin baik)
                sorted_scores = sorted(scores, key=lambda x: x.get('time', float('inf')))[:2]
                
                for idx, score in enumerate(sorted_scores, 1):
                    time_val = score.get('time', 0)
                    minutes = int(time_val) // 60
                    seconds = int(time_val) % 60
                    millisecs = int((time_val % 1) * 100)
                    
                    score_text = f"  {idx}. {minutes:02d}:{seconds:02d}.{millisecs:02d}"
                    score_surface = self.score_font.render(score_text, True, (200, 200, 255))
                    surface.blit(score_surface, (80, y_pos))
                    y_pos += 30
            else:
                no_score_text = self.score_font.render("  No scores yet", True, (150, 150, 150))
                surface.blit(no_score_text, (80, y_pos))
                y_pos += 30
            
            y_pos += level_spacing - 70  # Adjust spacing between level sections
        
        # Draw back button
        self.back_button.draw(surface)
