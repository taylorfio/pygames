import pygame
import random


class User:
    def __init__(self):
        self.image = pygame.Surface([30, 30])
        self.image.fill((0, 0, 0))
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


class Bullet:
    def __init__(self):
        self.image = pygame.Surface([10, 10])
        self.image.fill((0, 0, 0))
        self.x = 1000
        self.y = 1000
        self.x_change = 0
        self.y_change = 0


    def shoot(self, user, x_change, y_change):
        self.x = user.x
        self.y = user.y
        self.x_change = x_change
        self.y_change = y_change



    def draw(self, surface):
        surface.blit(self.image, (self.x, self.y))


class Enemy:
    def __init__(self):
        self.image = pygame.Surface([25, 25])
        self.image.fill((255, 0, 0))
        self.x = 0
        self.y = 0

        # dist = 15
        # make them follow and go towards user

    def spawn(self):
        spawn_spot = random.randint(0, 4)
        if spawn_spot == 0:
            self.x = 0
            self.y = 0
        if spawn_spot == 1:
            self.x = 800
            self.y = 0
        if spawn_spot == 2:
            self.x = 0
            self.y = 600
        if spawn_spot == 3:
            self.x = 800
            self.y = 600

    def draw(self, surface):
        surface.blit(self.image, (self.x, self.y))


pygame.init()
screen = pygame.display.set_mode((800, 600))
clock = pygame.time.Clock()
FPS = 30

user = User()
bullet_list = []
enemy = Enemy()

running = True
bullet_xchange = 0
bullet_ychange = 0
while running:
    clock.tick(FPS)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_k:
                bullet = Bullet()
                bullet.shoot(user,0, 60)
                bullet_list.append(bullet)
                print(bullet)
            if event.key == pygame.K_i:
                bullet = Bullet()
                bullet.shoot(user, 0, -60)
                bullet_list.append(bullet)
            if event.key == pygame.K_j:
                bullet = Bullet()
                bullet.shoot(user, -60, 0)
                bullet_list.append(bullet)
            if event.key == pygame.K_l:
                bullet = Bullet()
                bullet.shoot(user, 60, 0)
                bullet_list.append(bullet)

    if len(bullet_list)>0:
        print(bullet_list[0].y)
    for bullet in bullet_list:
        bullet.x += bullet.x_change
        bullet.y += bullet.y_change
        screen.blit(bullet.image, (bullet.x, bullet.y))

    user.keys_input()
    enemy.spawn()

    screen.fill((255, 255, 255))
    user.draw(screen)
    enemy.draw(screen)
    pygame.display.update()


# problems
# bullet needs to move until the end of the screen
# how to hit enemy sprite
# enemy needs to follow you
