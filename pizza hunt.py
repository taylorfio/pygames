import pygame
import random
from os import path

restart = True
while restart:

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
    pygame.display.set_caption("PAPA'S PIZZA HUNT")
    clock = pygame.time.Clock()

    font_name = pygame.font.match_font('arial')


    def draw_text(surface, text, size, x, y):
        font = pygame.font.Font(font_name, size)
        text_surface = font.render(text, True, WHITE)  # True means that the text will be anti-aliased
        text_rect = text_surface.get_rect()
        text_rect.midtop = (x, y)  # sets the texts position
        surface.blit(text_surface, text_rect)

    def start_screen():
        draw_text(screen, "PAPA'S PIZZA HUNT", 64, WIDTH / 2, HEIGHT / 4)
        draw_text(screen, "left and right arrow keys to move, up arrow key to fire", 22, WIDTH / 2, HEIGHT / 2)
        draw_text(screen, "Press a key to begin", 30, WIDTH / 2, HEIGHT * 3 / 4)
        draw_text(screen, "Press exit to quit", 18, WIDTH / 2, HEIGHT * 3 / 4 + 30)
        pygame.display.flip()
        waiting = True
        while waiting:
            clock.tick(FPS)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                elif event.type == pygame.KEYUP:
                    waiting = False

    def end_screen(score):
        draw_text(screen, "YOU LOST", 64, WIDTH / 2, HEIGHT / 4)
        end_text = "SCORE: " + str(score)
        draw_text(screen, end_text, 35, WIDTH / 2, HEIGHT / 2 - 100)
        draw_text(screen, "HIGH SCORE", 35, WIDTH / 2, HEIGHT / 2 - 30)

        try:
            file3 = open("save.txt", "r")
            line2 = str(file3.seek(0))
            file3.close()
        except IOError:
            line2 = "ERROR SCORE NOT FOUND"

        draw_text(screen, str(line2), 35, WIDTH / 2, HEIGHT / 2)

        draw_text(screen, "Press a key to restart", 30, WIDTH / 2, HEIGHT * 3 / 4)
        draw_text(screen, "Press exit to quit", 18, WIDTH / 2, HEIGHT * 3 / 4 + 30)
        pygame.display.flip()
        waiting = True
        while waiting:
            clock.tick(FPS)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                elif event.type == pygame.KEYUP:
                    waiting = False

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
    background = pygame.image.load(path.join(img_dir, "dark restaurant.jpg"))
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

    start_screen()  # runs the screen for when you begin the game

    # game loop
    running = True
    while running:

        clock.tick(FPS)  # keeps loop running at the right frame rate

        # process input (events)
        for event in pygame.event.get():  # checks for closing input
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame. K_UP:
                    player.shoot()

        all_sprites.update()  # updates the sprites

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
        screen.blit(background, (0,0))
        all_sprites.draw(screen)
        draw_text(screen, str(score), 50, WIDTH / 2, 10)

        pygame.display.flip()  # after it draws everything flip the display

    try:
        file1 = open("save.txt", "r")
        line1 = int(file1.seek(0))
        file1.close()
        file2 = open("save.txt", "w")
        if int(score) > int(line1):
            file2.write(str(score))
        end_screen(score)
        file2.close()
    except IOError:
        end_screen(score)

pygame.quit()

# score broke
