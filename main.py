# main.py
import pygame
from src.core import settings
from src.screen_manager import ScreenManager
from src.scene.main_menu import MainMenuScreen
from src.audio.sound_manager import init_sound_manager
from src.audio.bgm import play_background_music


def main():
    pygame.init()
    
    # Initialize sound manager
    init_sound_manager()

    screen_width = settings.WIDTH
    screen_height = settings.HEIGHT
    screen = pygame.display.set_mode((screen_width, screen_height))
    pygame.display.set_caption(settings.TITLE)

    clock = pygame.time.Clock()

    # Buat screen awal (Main Menu) dan ScreenManager
    main_menu = MainMenuScreen(None, screen_width, screen_height)
    manager = ScreenManager(main_menu)
    # Inject manager ke screen (agar bisa switch)
    main_menu.manager = manager

    play_background_music(volume=0.2)

    running = True
    while running:
        dt = clock.tick(60) / 1000.0

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            else:
                manager.handle_event(event)

        manager.update(dt)
        manager.draw(screen)
        pygame.display.flip()

    pygame.quit()


if __name__ == "__main__":
    main()