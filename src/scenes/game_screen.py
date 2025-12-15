import pygame
from .level_base import BaseScreen
from ..core.game import Game
from ..ui.button import Button
# from ..core.high_scores import HighScoreManager

class GameScreen(BaseScreen):
    def __init__(self, manager, screen_width: int, screen_height: int):
        super().__init__(manager, screen_width, screen_height)

        self.game = Game(screen_width, screen_height)

        # self.high_score_manager = HighScoreManager()
        # self._handled_game_over = False

        # Tombol Back to Menu (misal di pojok kanan atas)
        self.button_font = pygame.font.SysFont(None, 24)
        self.back_button = Button(
            pygame.Rect(screen_width - 150, 10, 140, 40),
            "Back to Menu",
            self.button_font,
            bg_color=(80, 80, 80),
            hover_color=(120, 120, 120),
        )

    def handle_event(self, event: pygame.event.Event):
        # Forward event ke Game jika suatu saat perlu (misal pause dsb.)
        self.game.handle_event(event)

        if self.back_button.handle_event(event):
            from .main_menu import MainMenuScreen
            new_screen = MainMenuScreen(self.manager, self.screen_width, self.screen_height)
            self.manager.switch_to(new_screen)

    def update(self, dt: float):
        self.game.update(dt)

        # if self.game.game_over and not self._handled_game_over:
        #     self._handled_game_over = True

        #     final_score = self.game.player.score

        #     # Untuk sementara, nama pemain kita isi default "PLAYER"
        #     self.high_score_manager.add_score("PLAYER", final_score)

        #     from .high_score import HighScoreScreen
        #     new_screen = HighScoreScreen(
        #         self.manager,
        #         self.screen_width,
        #         self.screen_height,
        #         recent_score=final_score,
        #     )
        #     self.manager.switch_to(new_screen)

    def draw(self, surface: pygame.Surface):
        self.game.draw(surface)
        self.back_button.draw(surface)
