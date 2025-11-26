import pygame
import sys

class Player:
    def __init__(self, x, y, color):
        self.x = x
        self.y = y
        self.size = 40
        self.color = color
        self.speed = 5

    def update(self, keys, controls):
        if keys[controls["up"]]:
            self.y -= self.speed
        if keys[controls["down"]]:
            self.y += self.speed
        if keys[controls["left"]]:
            self.x -= self.speed
        if keys[controls["right"]]:
            self.x += self.speed

    def draw(self, screen):
        pygame.draw.rect(screen, self.color,
                         (self.x, self.y, self.size, self.size))

class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((960, 540))
        pygame.display.set_caption("Eclipse Run")
        self.clock = pygame.time.Clock()
        self.running = True

        # dua player
        self.sun = Player(150, 250, (250, 210, 60))   # kuning
        self.moon = Player(150, 320, (140, 140, 220)) # ungu

    def run(self):
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False

            keys = pygame.key.get_pressed()
            # kontrol Sun: arrow
            self.sun.update(keys, {
                "up": pygame.K_UP,
                "down": pygame.K_DOWN,
                "left": pygame.K_LEFT,
                "right": pygame.K_RIGHT
            })
            # kontrol Moon: WASD
            self.moon.update(keys, {
                "up": pygame.K_w,
                "down": pygame.K_s,
                "left": pygame.K_a,
                "right": pygame.K_d
            })

            self.screen.fill((230, 230, 230))
            self.sun.draw(self.screen)
            self.moon.draw(self.screen)

            pygame.display.flip()
            self.clock.tick(60)

        pygame.quit()
        sys.exit()