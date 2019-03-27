import pygame
import random

WIDTH = 360
HEIGHT = 480
FPS = 30

#colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

# initialize pygame and creates window
pygame.init()
pygame.mixer.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("My Game")
clock = pygame.time.Clock()

all_sprites = pygame.sprite.Group()


class User:
    def __init__(self):
        self.image = pygame.Surface([30, 30])
        self.image.fill(WHITE)
        self.x = 400
        self.y = 300

    def keys_input(self):
        key = pygame.key.get_pressed()
        dist = 15
        if key[pygame.K_s]:
            user.y += dist
        elif key[pygame.K_w]:
            user.y -= dist
        if key[pygame.K_d]:
            user.x += dist
        elif key[pygame.K_a]:
            user.x -= dist

    def draw(self, surface):
        surface.blit(self.image, (self.x, self.y))






# Game loop
running = True
while running:
    clock.tick(FPS)  # keeps the loop running at the right speed
    for event in pygame.event.get():  # Process input
        if event.type == pygame.QUIT:  # checks for closing window
            running = False

    user = User()


    all_sprites.update()
    user.keys_input()

    screen.fill(BLACK)

    user.draw(screen)
    all_sprites.draw(screen)
    pygame.display.flip()

pygame.quit()