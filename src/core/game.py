# src/core/game.py
import pygame
import sys
from src.core import settings
from src.scene.level1 import Level1
from src.scene.level2 import Level2
from src.scene.level3 import Level3
from src.systems.pov import POVController


class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((settings.WIDTH, settings.HEIGHT))
        pygame.display.set_caption("Eclipse Run")
        self.clock = pygame.time.Clock()
        self.running = True
        self.pov = POVController()
        
        self.current_level = 1
        self.scene = None
        self.load_level(1)

    def load_level(self, level_num):
        # Load level berdasarkan nomor
        self.current_level = level_num
        
        if level_num == 1:
            self.scene = Level1(self)
        elif level_num == 2:
            self.scene = Level2(self)
        elif level_num == 3:
            self.scene = Level3(self)
        else:
            return
        
        self.pov.mode = self.pov.mode.__class__.SIDE

    def next_level(self):
        # lanjutt level
        next_level = self.current_level + 1
        if next_level <= 3:
            self.load_level(next_level)
        else:
            self.load_level(1)

    def run(self):
        # game loop
        while self.running:
            dt = self.clock.tick(settings.FPS)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False

                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        self.running = False
                    
                    elif event.key == pygame.K_SPACE:
                        self.pov.toggle()
                    
                if self.scene:
                    self.scene.handle_event(event)

            if self.scene:
                self.scene.update(dt)
                self.scene.draw(self.screen)
            
            pygame.display.flip()

        pygame.quit()
        sys.exit()