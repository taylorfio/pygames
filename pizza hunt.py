import pygame
import random
from os import path

restart = True
while restart:  # loop for game

    img_dir = path.join(path.dirname(__file__), 'img')  # path for images
    snd_dir = path.join(path.dirname(__file__), 'snd')  # path for sounds

    WIDTH = 480  # sets size
    HEIGHT = 600
    FPS = 60  # sets the frames per second
    POWERUP_TIME = 2000  # milliseconds, time for powerup

    # colors
    WHITE = (255, 255, 255)
    BLACK = (0, 0, 0)
    RED = (255, 0, 0)
    GREEN = (0, 255, 0)
    BLUE = (0, 0, 255)
    YELLOW = (255, 255, 0)

    # initialize pygame and create window
    pygame.init()  # loads pygame
    pygame.mixer.init()  # loads the sounds
    screen = pygame.display.set_mode((WIDTH, HEIGHT))  # sets the screen dimensions
    pygame.display.set_caption("PAPA'S PIZZA HUNT")  # window name
    clock = pygame.time.Clock()  # sets game clock

    font_name = pygame.font.match_font('arial')  # sets font


    def draw_text(surface, text, size, x, y):  # function for drawing text on the screen
        font = pygame.font.Font(font_name, size)
        text_surface = font.render(text, True, WHITE)  # True means that the text will be anti-aliased
        text_rect = text_surface.get_rect()
        text_rect.midtop = (x, y)  # sets the texts position
        surface.blit(text_surface, text_rect)

    def start_screen():
        draw_text(screen, "PAPA'S PIZZA HUNT", 64, WIDTH / 2, HEIGHT / 4)  # draws text
        draw_text(screen, "left and right arrow keys to move, up arrow key to fire", 22, WIDTH / 2, HEIGHT / 2)
        draw_text(screen, "Press a key to begin", 30, WIDTH / 2, HEIGHT * 3 / 4)
        draw_text(screen, "Press exit to quit", 18, WIDTH / 2, HEIGHT * 3 / 4 + 30)
        pygame.display.flip()
        waiting = True
        while waiting:  # waits for input
            clock.tick(FPS)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:  # if exit is pressed it quits
                    pygame.quit()
                elif event.type == pygame.KEYUP:  # if any other key is pressed game starts
                    waiting = False

    def end_screen(score):
        draw_text(screen, "YOU LOST", 64, WIDTH / 2, HEIGHT / 4)   # draws text
        end_text = "SCORE: " + str(score)  # shows game score
        draw_text(screen, end_text, 35, WIDTH / 2, HEIGHT / 2 - 100)
        draw_text(screen, "HIGH SCORE", 35, WIDTH / 2, HEIGHT / 2 - 30)

        try:
            file1 = open("save.txt", "r")
            line1 = file1.read()
            line1 = int(line1)
            file1.close()
            file2 = open("save.txt", "w")
            if int(score) > int(line1):
                file2.write(str(score))
                number = score
            else:
                file2.write(str(line1))
                number = line1
            file2.close()
        except IOError:
            number = "ERROR SCORE NOT FOUND"

        draw_text(screen, str(number), 35, WIDTH / 2, HEIGHT / 2)

        draw_text(screen, "Press a key to restart", 30, WIDTH / 2, HEIGHT * 3 / 4)
        draw_text(screen, "Press exit to quit", 18, WIDTH / 2, HEIGHT * 3 / 4 + 30)
        pygame.display.flip()
        waiting = True
        while waiting:  # waits for input
            clock.tick(FPS)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:  # if exit is pressed it quits
                    pygame.quit()
                elif event.type == pygame.KEYUP:  # if any other key is pressed game starts
                    waiting = False

    class Player(pygame.sprite.Sprite):
        def __init__(self):
            pygame.sprite.Sprite.__init__(self)
            self.image = pygame.transform.scale(player_img, (90, 104))  # sets the sprite image and scales it down
            self.image.set_colorkey(BLACK)  # eliminates the black filler colour from the png
            self.rect = self.image.get_rect()  # sets the hit box for sprite
            self.rect.centerx = WIDTH / 2  # when the game starts and this function is called the position is set to the middle
            self.rect.bottom = HEIGHT - 10  # when the game starts and this function is called the position is set to just above the bottom
            # powerup
            self.power = 1  # sets base power level
            self.power_time = pygame.time.get_ticks()  # timer to know when to go back to normal

        def update(self):
            # timeout for powerups
            # if howerver long its been since the getting the power up is greater then the amount of time
            if self.power >= 2 and pygame.time.get_ticks() - self.power_time > POWERUP_TIME:
                self.power -= 1  # brings you back to normal power
                self.power_time = pygame.time.get_ticks()  # resets the timer

            self.speedx = 0  # sets the speed to nothing if nothing is being pressed
            keystate = pygame.key.get_pressed()  # variable for what key is being pressed
            if keystate[pygame.K_LEFT]:  # if left key pressed down
                self.speedx = -15  # moves left
            if keystate[pygame.K_RIGHT]:  # if right key pressed down
                self.speedx = 15  # moves right
            self.rect.x += self.speedx  # sets the sprite to move in what direction is pressed
            if self.rect.right > WIDTH:
                self.rect.right = WIDTH  # stops it from moving of the screen right
            if self.rect.left < 0:
                self.rect.left = 0  # stops it from moving of the screen left

        def shoot(self):
            if self.power == 1:  # normal state for shooting
                bullet = Bullet(self.rect.centerx, self.rect.top)  # sets the bullet to the center of the sprite
                all_sprites.add(bullet)  # whenever the bullet spawns it is added to the list so multiple can be on the screen
                bullets.add(bullet)
                shoot_sound.play()  # plays the shooting sound
            if self.power == 2:  # powered state for shooting
                bullet1 = Bullet(self.rect.left, self.rect.centery)  # spawns three bullets in right, left and canter
                bullet2 = Bullet(self.rect.right, self.rect.centery)
                bullet3 = Bullet(self.rect.centerx, self.rect.centery)
                all_sprites.add(bullet1)
                all_sprites.add(bullet2)  # adds three bullets to right, left and canter
                all_sprites.add(bullet3)
                bullets.add(bullet1)
                bullets.add(bullet2)
                bullets.add(bullet3)
                shoot_sound.play()  # plays shooting sound

        def powerup(self):
            if self.power < 2:  # stops the powers variable from getting more then 2
                self.power += 1  # changes the power variable
                self.power_time = pygame.time.get_ticks()  # sets timer


    class Enemy(pygame.sprite.Sprite):
        def __init__(self):
            pygame.sprite.Sprite.__init__(self)
            self.image = pygame.transform.scale(enemy_img, (60, 69))  # sets the sprite image and scales it down
            self.image.set_colorkey(BLACK)  # eliminates the black filler colour from the png
            self.rect = self.image.get_rect()  # sets the hit box for sprite
            self.rect.x = random.randrange(0, WIDTH - self.rect.width)  # spawns the sprite in a random spot on the top of the screen
            self.rect.y = random.randrange(-100, -40)
            self.speedy = random.randrange(5, 15)  # random speed downwards
            self.speedx = random.randrange(-3, 3)  # random speed sideways

        def update(self):
            self.rect.x += self.speedx  # updates the position of the sprite by what it is moving by
            self.rect.y += self.speedy
            if self.rect.top > HEIGHT + 10 or self.rect.left < -25 or self.rect.right > WIDTH + 20:  # if the top of the sprite is below the bottom it respawns at the top
                self.rect.x = random.randrange(0, WIDTH - self.rect.width)
                self.rect.y = random.randrange(-100, -40)  # respawns it
                self.speedy = random.randrange(1, 8)


    class Bullet(pygame.sprite.Sprite):
        def __init__(self, x, y):
            pygame.sprite.Sprite.__init__(self)
            self.image = pygame.transform.scale(bullet_img, (20, 35))  # sets the sprite image and scales it down
            self.image.set_colorkey(BLACK)  # eliminates the black filler colour from the png
            self.rect = self.image.get_rect()  # sets the hit box for sprite
            self.rect.bottom = y  # sets y coordinates
            self.rect.centerx = x  # sets x coordinates
            self.speedy = -30  # sets the rate at which it moves up

        def update(self):
            self.rect.y += self.speedy
            if self.rect.bottom < 0:  # kills if it moves off the top of the screen
                self.kill()


    class Powerup(pygame.sprite.Sprite):
        def __init__(self, center):
            pygame.sprite.Sprite.__init__(self)
            self.image = powerup_img  # sets the sprite image and scales it down
            self.image.set_colorkey(BLACK)  # eliminates the black filler colour from the png
            self.rect = self.image.get_rect()  # sets the hit box for sprite
            self.rect.center = center
            self.speedy = 20

        def update(self):
            self.rect.y += self.speedy
            if self.rect.top > HEIGHT:  # kill if it moves off the bottom of the screen
                self.kill()


    class Boss(pygame.sprite.Sprite):
        def __init__(self):
            pygame.sprite.Sprite.__init__(self)
            self.image = pygame.transform.scale(calzone_img, (200, 100))  # sets the sprite image and scales it down
            self.image.set_colorkey(BLACK)  # eliminates the black filler colour from the png
            self.rect = self.image.get_rect()  # sets the hit box for sprite
            self.rect.x = random.randrange(0, WIDTH - self.rect.width)  # spawns the sprite in a random spot on the top of the screen
            self.rect.y = random.randrange(-100, -40)
            self.speedy = 20  # rate the sprite moves down

        def update(self):
            self.rect.y += self.speedy  # moves the sprite at the given rate
            if self.rect.top > HEIGHT + 10 or self.rect.left < -25 or self.rect.right > WIDTH + 20:  # if the top of the sprite is below the bottom it respawns at the top
                self.rect.x = random.randrange(0, WIDTH - self.rect.width)
                self.rect.y = random.randrange(-100, -40)  # respawns it
                self.speedy = random.randrange(1, 8)


    # loads all the game graphics
    # .convert() converts the image to the same pixel format as the display
    background = pygame.image.load(path.join(img_dir, "dark restaurant.jpg")).convert()
    player_img = pygame.image.load(path.join(img_dir, 'pappa.png')).convert()
    enemy_img = pygame.image.load(path.join(img_dir, 'PizzaSlice.png')).convert()
    bullet_img = pygame.image.load(path.join(img_dir, 'lightninbolt.png')).convert()
    powerup_img = pygame.image.load(path.join(img_dir, 'bolt.png')).convert()
    calzone_img = pygame.image.load(path.join(img_dir, 'calzone.png')).convert()

    # loads all the game sounds
    pygame.mixer.music.set_volume(0.4)
    pygame.mixer.music.load(path.join(snd_dir, 'melody.mp3'))
    shoot_sound = pygame.mixer.Sound(path.join(snd_dir, 'pew.wav'))
    explosion_sounds = []
    for sound in ['expl3.wav', 'expl6.wav']:  # adds to sounds to list to randomly be selected
        explosion_sounds.append(pygame.mixer.Sound(path.join(snd_dir, sound)))

    # puts the sprites in groups to easily call them
    all_sprites = pygame.sprite.Group()
    player = Player()
    all_sprites.add(player)
    enemy = pygame.sprite.Group()
    bullets = pygame.sprite.Group()
    powerups = pygame.sprite.Group()
    boss = pygame.sprite.Group()
    for amount in range(8):  # creates 10 sprites
        m = Enemy()
        all_sprites.add(m)
        enemy.add(m)

    score = 0  # sets score
    pygame.mixer.music.play(loops=-1)  # tells pygame to loop music when it reaches the end

    start_screen()  # runs the screen for when you begin the game

    # game loop
    running = True
    while running:

        clock.tick(FPS)  # keeps loop running at the right frame rate

        # process the input (events)
        for event in pygame.event.get():  # checks for closing exit input
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:  # filter for any keyboard input
                if event.key == pygame. K_UP:  # if up key down
                    player.shoot()  # shoots bullet

        all_sprites.update()  # updates the sprites

        # checks to see if a bullet hits a enemy
        hits = pygame.sprite.groupcollide(enemy, bullets, True, True)
        for hit in hits:  # every time a bullet hits an enemy
            random.choice(explosion_sounds).play()  # plays explosion sound
            score += 1  # increases score
            m = Enemy()
            all_sprites.add(m)  # respawns the sprite
            enemy.add(m)

            # every time you hit an enemy there is a chance to spawn the boss
            boss_spawn = random.randint(1, 20)
            if boss_spawn == 1:  # picks a random between 1 and 20 creating a 5% chance
                b = Boss()
                all_sprites.add(boss)  # spawns sprite
                boss.add(b)
            # every time you hit an enemy there is a chance to spawn a power up
            if random.random() > 0.9:  # picks a random decimal number between 0 and 1 creating a 10% chance
                powerup = Powerup(hit.rect.center)  # spawns the sprite where the enemy was killed
                all_sprites.add(powerup)  # spawns sprite
                powerups.add(powerup)

        # checks to see if a bullet hits the boss
        boss_hits = pygame.sprite.groupcollide(boss, bullets, True, True)
        for hit in boss_hits:  # if boss is hit
            random.choice(explosion_sounds).play()  # plays explosion sound
            score += 50  # increases score
            b = Boss()
            all_sprites.remove(boss)  # removes the boss
            boss.remove(b)

        # checks to see if player hits a powerup
        hits = pygame.sprite.spritecollide(player, powerups, True)
        for hit in hits:  # if powerup hits player
            player.powerup()  # runs the powerup

        # checks to see if enemy hits player
        collision = pygame.sprite.spritecollide(player, enemy, False)
        if collision:  # if enemy hits player
            running = False  # ends game

        # checks to see if boss hits player
        collision = pygame.sprite.spritecollide(player, boss, False)
        if collision:  # if boss hits player
            running = False  # ends game

        # Draw / render
        screen.fill(BLACK)  # fills the screen with black behind the image
        screen.blit(background, (0, 0))  # sets the background image to center
        all_sprites.draw(screen)  # shows the sprites
        draw_text(screen, str(score), 50, WIDTH / 2, 10)  # shows the current score

        pygame.display.flip()  # after it draws everything flip the display

    end_screen(score)  # plays the end screen

pygame.quit()
