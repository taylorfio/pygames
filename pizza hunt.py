import pygame
import random
from os import path

img_dir = path.join(path.dirname(__file__), 'img')
snd_dir = path.join(path.dirname(__file__), 'snd')

WIDTH = 480
HEIGHT = 600
FPS = 60

# define colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)

# initialize pygame and create window
pygame.init()  # loads pygame
pygame.mixer.init()  # loads the sounds
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("shooter game")
clock = pygame.time.Clock()

font_name = pygame.font.match_font('arial')


def draw_text(surface, text, size, x, y):
    font = pygame.font.Font(font_name, size)
    text_surface = font.render(text, True, WHITE)  # True means that the text will be anti-aliased
    text_rect = text_surface.get_rect()
    text_rect.midtop = (x, y)  # sets the texts position
    surface.blit(text_surface, text_rect)


class Player(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.transform.scale(player_img, (90, 104))
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.centerx = WIDTH / 2
        self.rect.bottom = HEIGHT - 10
        self.speedx = 0

    def update(self):
        self.speedx = 0
        keystate = pygame.key.get_pressed()
        if keystate[pygame.K_LEFT]:
            self.speedx = -15
        if keystate[pygame.K_RIGHT]:
            self.speedx = 15
        self.rect.x += self.speedx
        if self.rect.right > WIDTH:
            self.rect.right = WIDTH
        if self.rect.left < 0:
            self.rect.left = 0

    def shoot(self):
        bullet = Bullet(self.rect.centerx, self.rect.top)
        all_sprites.add(bullet)
        bullets.add(bullet)
        shoot_sound.play()


class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.transform.scale(enemy_img, (60, 69))
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.x = random.randrange(0, WIDTH - self.rect.width)
        self.rect.y = random.randrange(-100, -40)
        self.speedy = random.randrange(5, 15)
        self.speedx = random.randrange(-3, 3)

    def update(self):
        self.rect.x += self.speedx
        self.rect.y += self.speedy
        if self.rect.top > HEIGHT + 10 or self.rect.left < -25 or self.rect.right > WIDTH + 20:
            self.rect.x = random.randrange(0, WIDTH - self.rect.width)
            self.rect.y = random.randrange(-100, -40)
            self.speedy = random.randrange(1, 8)


class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.transform.scale(bullet_img, (20, 35))
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.bottom = y
        self.rect.centerx = x
        self.speedy = -30

    def update(self):
        self.rect.y += self.speedy
        if self.rect.bottom < 0:  # kills if it moves off the top of the screen
            self.kill()


# loads all the game graphics
#background = pygame.image.load(path.join(img_dir, "whitewall.jpg")).convert
#background_rect = background.get_rect()
player_img = pygame.image.load(path.join(img_dir, 'pappa.png')).convert()
enemy_img = pygame.image.load(path.join(img_dir, 'PizzaSlice.png')).convert()
bullet_img = pygame.image.load(path.join(img_dir, 'lightninbolt.png')).convert()

# loads all the game sounds
pygame.mixer.music.set_volume(0.4)
pygame.mixer.music.load(path.join(snd_dir, 'i am a pizza.mp3'))
shoot_sound = pygame.mixer.Sound(path.join(snd_dir, 'pew.wav'))
explosion_sounds = []
for sound in ['expl3.wav', 'expl6.wav']:
    explosion_sounds.append(pygame.mixer.Sound(path.join(snd_dir, sound)))

all_sprites = pygame.sprite.Group()
player = Player()
enemy = pygame.sprite.Group()
bullets = pygame.sprite.Group()
all_sprites.add(player)
for amount in range(8):
    m = Enemy()
    all_sprites.add(m)
    enemy.add(m)

score = 0
pygame.mixer.music.play(loops=-1)  # tells pygame to loop music when it reaches the end

# game loop
running = True
while running:
    # keep loop running at the right speed
    clock.tick(FPS)
    # Process input (events)
    for event in pygame.event.get():
        # check for closing window
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame. K_UP:
                player.shoot()

    # update
    all_sprites.update()

    # checks to see if a bullet hit a mob
    hits = pygame.sprite.groupcollide(enemy, bullets, True, True)
    for hit in hits:
        random.choice(explosion_sounds).play()
        score += 1
        m = Enemy()
        all_sprites.add(m)
        enemy.add(m)

    # checks to see if mob hit player
    collision = pygame.sprite.spritecollide(player, enemy, False)
    if collision:
        running = False

    # Draw / render
    screen.fill(BLACK)
    #screen.blit(background, background_rect)
    all_sprites.draw(screen)
    draw_text(screen, str(score), 50, WIDTH / 2, 10)

    pygame.display.flip()  # after it draws everything flip the display

pygame.quit()