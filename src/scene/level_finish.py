import os
import json
import datetime
import pygame
from .base_screen import BaseScreen
from ..ui.button import Button

BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
IMAGE_DIR = os.path.join(BASE_DIR, "assets", "images", "ui")
MENU_BACKGROUND_IMAGE = "menu_bg.jpeg"
HIGH_SCORES_FILE = os.path.join(BASE_DIR, "assets", "data", "high_scores.json")


class LevelFinishScreen(BaseScreen):
    def __init__(self, manager, screen_width, screen_height, level_num=1, time_elapsed=0.0):
        super().__init__(manager, screen_width, screen_height)
        
        self.level_num = level_num
        self.time_elapsed = time_elapsed
        self.background_color = (20, 20, 30)
        
        # Save high score
        self._save_high_score(level_num, time_elapsed)
        
        # Load background image
        self.background_image = None
        bg_path = os.path.join(IMAGE_DIR, MENU_BACKGROUND_IMAGE)
        try:
            bg = pygame.image.load(bg_path).convert_alpha()
            self.background_image = pygame.transform.smoothscale(bg, (screen_width, screen_height))
        except Exception as e:
            print(f"Warning: failed to load background '{bg_path}': {e}")
        
        # Fonts
        self.title_font = pygame.font.SysFont(None, 72, bold=True)
        self.time_font = pygame.font.SysFont(None, 48)
        self.button_font = pygame.font.SysFont(None, 32)
        
        # Button layout
        button_width = 220
        button_height = 50
        center_x = screen_width // 2
        start_y = screen_height // 2 + 80
        
        # Next Level Button
        self.next_button = Button(
            pygame.Rect(center_x - button_width // 2, start_y, button_width, button_height),
            "Next Level" if level_num < 3 else "Finish",
            self.button_font,
            bg_color=(70, 160, 70),
            hover_color=(100, 200, 100)
        )
        
        # Back to Level Select Button
        self.back_button = Button(
            pygame.Rect(center_x - button_width // 2, start_y + 70, button_width, button_height),
            "Level Select",
            self.button_font,
            bg_color=(70, 100, 160),
            hover_color=(100, 150, 200)
        )
        
        # Main Menu Button
        self.menu_button = Button(
            pygame.Rect(center_x - button_width // 2, start_y + 140, button_width, button_height),
            "Main Menu",
            self.button_font,
            bg_color=(160, 100, 70),
            hover_color=(200, 150, 100)
        )
    
    def handle_event(self, event: pygame.event.Event):
        if self.next_button.handle_event(event):
            if self.level_num < 3:
                from .level1 import Level1
                from .level2 import Level2
                from .level3 import Level3
                
                if self.level_num == 1:
                    next_screen = Level2(self.manager, self.screen_width, self.screen_height)
                elif self.level_num == 2:
                    next_screen = Level3(self.manager, self.screen_width, self.screen_height)
                else:
                    next_screen = Level1(self.manager, self.screen_width, self.screen_height)
            else:
                # Level 3 selesai, kembali ke main menu
                from .main_menu import MainMenuScreen
                next_screen = MainMenuScreen(self.manager, self.screen_width, self.screen_height)
            
            self.manager.switch_to(next_screen)
        
        if self.back_button.handle_event(event):
            from .level_select import LevelSelectScreen
            self.manager.switch_to(LevelSelectScreen(self.manager, self.screen_width, self.screen_height))
        
        if self.menu_button.handle_event(event):
            from .main_menu import MainMenuScreen
            self.manager.switch_to(MainMenuScreen(self.manager, self.screen_width, self.screen_height))
    
    def update(self, dt: float):
        pass
    
    def draw(self, surface: pygame.Surface):
        # Draw background
        if self.background_image:
            surface.blit(self.background_image, (0, 0))
            overlay = pygame.Surface((self.screen_width, self.screen_height), pygame.SRCALPHA)
            overlay.fill((0, 0, 0, 80))
            surface.blit(overlay, (0, 0))
        else:
            surface.fill(self.background_color)
        
        # Draw "LEVEL CLEAR"
        title_text = f"LEVEL {self.level_num} CLEAR!"
        title_surface = self.title_font.render(title_text, True, (100, 255, 100))
        title_rect = title_surface.get_rect(center=(self.screen_width // 2, 80))
        surface.blit(title_surface, title_rect)
        
        # Format time (MM:SS format)
        minutes = int(self.time_elapsed) // 60
        seconds = int(self.time_elapsed) % 60
        time_text = f"Time: {minutes:02d}:{seconds:02d}"
        
        time_surface = self.time_font.render(time_text, True, (255, 255, 100))
        time_rect = time_surface.get_rect(center=(self.screen_width // 2, 180))
        surface.blit(time_surface, time_rect)
        
        # Draw buttons
        self.next_button.draw(surface)
        self.back_button.draw(surface)
        self.menu_button.draw(surface)
    
    def _save_high_score(self, level_num, time_elapsed):
        """Save high score untuk level yang selesai"""
        try:
            data_dir = os.path.dirname(HIGH_SCORES_FILE)
            os.makedirs(data_dir, exist_ok=True)
            
            # Load existing scores
            scores_data = {}
            if os.path.exists(HIGH_SCORES_FILE):
                with open(HIGH_SCORES_FILE, 'r') as f:
                    scores_data = json.load(f)
            
            # Ensure level keys exist
            for i in range(1, 4):
                if f"level_{i}" not in scores_data:
                    scores_data[f"level_{i}"] = []
            
            # Add new score
            level_key = f"level_{level_num}"
            scores_data[level_key].append({
                "time": time_elapsed,
                "timestamp": str(datetime.datetime.now())
            })
            
            # Keep only top 2 scores per level (sorted by time, fastest first)
            scores_data[level_key] = sorted(
                scores_data[level_key],
                key=lambda x: x.get('time', float('inf'))
            )[:2]
            
            # Save back to file
            with open(HIGH_SCORES_FILE, 'w') as f:
                json.dump(scores_data, f, indent=2)
            
            print(f"High score saved for level {level_num}: {time_elapsed:.2f}s")
        except Exception as e:
            print(f"Error saving high score: {e}")
