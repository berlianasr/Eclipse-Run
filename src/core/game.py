# src/core/game.py
import pygame
import sys
from src.core import settings
from src.scene.level1 import Level1
from src.systems.pov import POVController, POVMode



class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((settings.WIDTH, settings.HEIGHT))
        pygame.display.set_caption("Eclipse Run")
        self.clock = pygame.time.Clock()
        self.running = True
        self.pov = POVController()


        # langsung main ke Level1
        self.scene = Level1(self)

    def run(self):
        while self.running:
            dt = self.clock.tick(settings.FPS)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                  running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        running = False
                    elif event.key == pygame.K_SPACE:
                        self.pov.toggle()


            self.scene.update(dt)
            self.scene.draw(self.screen)
            pygame.display.flip()

        pygame.quit()
        sys.exit()
