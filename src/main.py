import pygame
from .screen_manager import ScreenManager
from .scenes.main_menu import MainMenuScreen


def main():
    pygame.init()

    screen_width = 800
    screen_height = 600
    screen = pygame.display.set_mode((screen_width, screen_height))
    pygame.display.set_caption("Eclipse Run")

    clock = pygame.time.Clock()

    # Buat screen awal (Main Menu) dan ScreenManager
    main_menu = MainMenuScreen(None, screen_width, screen_height)
    manager = ScreenManager(main_menu)
    # Inject manager ke screen (agar bisa switch)
    main_menu.manager = manager

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
