import math
import random

import pygame
from pygame import mixer


class Player:
    frame = 0
    maxframe = 4
    bufferi = 0
    buffer = 10
    frames = [pygame.image.load('kid_idle.png'), pygame.image.load("kid_left.png"),pygame.image.load("kid_idle.png"), pygame.image.load("kid_right.png")]
    dam_frames = [pygame.image.load("kid_damage.png"), pygame.image.load("kid_left_dam.png"),pygame.image.load("kid_damage.png"), pygame.image.load("kid_right_dam.png")]
    damage = False
    damagevalue = 2
    mask = False
    health = 200
    posx = 400-32
    posy = 500+32
    hitx = 64
    hity = 64

    def gethitbox(self):
        return self.hitx, self.hity

    def getframe(self):
        return self.frame

    def isdamage(self):
        return self.damage

    def ismask(self):
        return self.mask



    def update_frame(self):
        self.bufferi += 1
        if self.bufferi == self.buffer:
            self.frame += 1
            self.bufferi = 0
            if self.frame == self.maxframe:
                self.frame = 0

    def getpos(self):
        return self.posx, self.posy

    def update_pos(self, x, y):
        self.posx = x
        self.posy = y



    def damaging(self):
        if self.damage and not self.mask:
            self.health -= self.damagevalue


class Enemy:
    frame = 0
    maxframe = 2
    bufferi = 0
    buffer = 10
    frames = [pygame.image.load("karen_left.png"), pygame.image.load("karen_right.png")]
    radius = 256
    posx = 0
    posy = 0
    hitx = 128
    hity = 128
    vx = 4
    vy = 40
    def gethitbox(self):
        return self.hitx, self.hity

    def getframe(self):
        return self.frame

    def getposx(self):
        return self.posx
    def getposy(self):
        return self.posy

    def getradius(self):
        return self.radius

    def update_frame(self):
        self.bufferi += 1
        if self.bufferi == self.buffer:
            self.frame += 1
            self.bufferi = 0
            if self.frame == self.maxframe:
                self.frame = 0

    def update_posx(self, x):
        self.posx += x

    def update_posy(self, y):
        self.posy += y

    def getpos(self):
        return self.posx, self.posy

    def update_pos(self, x, y):
        self.posx = x
        self.posy = y

    def getspeed(self):
        return self.vx, self.vy
    def setspeedx(self, x):
        self.vx = x
    def setspeedy(self, y):
        self.vy = y

class Item:
    posx = 0
    posy = 0
    hitx = 64
    hity = 64
    protection = 30

    def gethitbox(self):
        return self.hitx, self.hity

    def getsheild(self):
        return self.protection

    def getposx(self):
        return self.posx
    def getposy(self):
        return self.posy

    def update_posx(self, x):
        self.posx += x

    def update_posy(self, y):
        self.posy += y

    def getpos(self):
        return self.posx, self.posy

    def update_pos(self, x, y):
        self.posx = x
        self.posy = y

class Background:
    frame = 0
    maxframe = 7
    bufferi = 0
    buffer = 10
    bounds = 74
    x = 800
    y = 600
    frames = [pygame.image.load("background0.png"), pygame.image.load("background1.png"),pygame.image.load("background2.png"),pygame.image.load("background3.png"),pygame.image.load("background4.png"), pygame.image.load("background5.png"), pygame.image.load("background6.png")]

    def getframe(self):
        return self.frame

    def update_frame(self):
        self.bufferi += 1
        if self.bufferi == self.buffer:
            self.frame += 1
            self.bufferi = 0
            if self.frame == self.maxframe:
                self.frame = 0

def main():
    # Intialize the pygame
    pygame.init()

    # create the screen
    screen = pygame.display.set_mode((800, 600))

    # Background
    background = Background()

    # Sound
    mixer.music.load("background.wav")
    mixer.music.play(-1)

    # Caption and Icon
    pygame.display.set_caption("Space Invader")
    icon = pygame.image.load('ufo.png')
    pygame.display.set_icon(icon)

    # Player
    # playerImg = pygame.image.load('player.png')
    # playerX = 370
    # playerY = 480
    # playerX_change = 0
    player1 = Player()

    # Enemy
    evilarr = []
    # enemyImg = []
    # enemyX = []
    # enemyY = []
    # enemyX_change = []
    # enemyY_change = []
    num_of_enemies = 6

    for i in range(num_of_enemies):
        evilarr.append(Enemy())
        evilarr[i].update_pos(random.randint(0, 736), random.randint(50, 150))
    #    enemyImg.append(pygame.image.load('enemy.png'))
    #    enemyX.append(random.randint(0, 736))
    #    enemyY.append(random.randint(50, 150))
    #    enemyX_change.append(4)
    #    enemyY_change.append(40)

    # Bullet

    # Ready - You can't see the bullet on the screen
    # Fire - The bullet is currently moving

    bulletImg = pygame.image.load('bullet.png')
    bulletX = 0
    bulletY = 480
    bulletX_change = 0
    bulletY_change = 10
    bullet_state = "ready"

    # Score

    score_value = 0
    font = pygame.font.Font('freesansbold.ttf', 32)

    textX = 10
    testY = 10

    # Game Over
    over_font = pygame.font.Font('freesansbold.ttf', 64)

    def show_score(x, y):
        score = font.render("Score : " + str(score_value), True, (255, 255, 255))
        screen.blit(score, (x, y))

    def game_over_text():
        over_text = over_font.render("GAME OVER", True, (255, 255, 255))
        screen.blit(over_text, (200, 250))

    def player(x, y):
        screen.blit(player1.frames[player1.frame], (x, y))
        player1.update_frame()

    def enemy(x, y, i):
        screen.blit(evilarr[i].frames[evilarr[i].frame], (x, y))
        evilarr[i].update_frame()

    def fire_bullet(x, y):
        global bullet_state
        bullet_state = "fire"
        screen.blit(bulletImg, (x + 16, y + 10))

    def isCollision(enemyX, enemyY, bulletX, bulletY):
        distance = math.sqrt(math.pow(enemyX - bulletX, 2) + (math.pow(enemyY - bulletY, 2)))
        if distance < 27:
            return True
        else:
            return False

    # Game Loop

    running = True
    while running:

        # RGB = Red, Green, Blue
        screen.fill((0, 0, 0))
        # Background Image
        screen.blit(background.frames[background.frame], (0, 0))
        playerX_change = 0
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            # if keystroke is pressed check whether its right or left
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    # player1.update_pos(-5,0)
                    playerX_change = -5
                if event.key == pygame.K_RIGHT:
                    # player1.update_pos(5,0)
                    playerX_change = 5
                if event.key == pygame.K_SPACE:
                    if bullet_state is "ready":
                        bulletSound = mixer.Sound("laser.wav")
                        bulletSound.play()
                        # Get the current x cordinate of the spaceship
                        bulletX, temp = player1.getpos()

                        fire_bullet(bulletX, bulletY)

            if event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                    playerX_change = 0

        # 5 = 5 + -0.1 -> 5 = 5 - 0.1
        # 5 = 5 + 0.1
        playerX, playerY = player1.getpos()
        playerX += playerX_change
        if playerX <= 0:
            playerX = 0
        elif playerX >= 736:
            playerX = 736

        player1.update_pos(playerX, playerY)

        # Enemy Movement
        for i in range(num_of_enemies):

            # Game Over
            enemyX, enemyY = evilarr[i].getpos()
            if enemyY > 440:
                for j in range(num_of_enemies):
                    enemyX, enemyY = evilarr[j].getpos()
                    evilarr[i].update_pos(enemyX, 2000)
                game_over_text()
                break
            enemyX_change, enemyY_change = evilarr[i].getspeed()
            enemyX += enemyX_change

            if enemyX <= 0:
                evilarr[i].setspeedx(4)
                # enemyX_change = 4
                evilarr[i].update_pos(enemyX, enemyY)
            elif enemyX >= 736:
                evilarr[i].setspeedx(-4)
                # enemyX_change = -4
                evilarr[i].update_pos(enemyX, enemyY)

            # Collision
            collision = isCollision(enemyX, enemyY, bulletX, bulletY)
            if collision:
                explosionSound = mixer.Sound("explosion.wav")
                explosionSound.play()
                bulletY = 480
                bullet_state = "ready"
                score_value += 1
                evilarr[i].update_pos(random.randint(0, 736), random.randint(50, 150))

            enemy(enemyX, enemyY, i)

        # Bullet Movement
        if bulletY <= 0:
            bulletY = 480
            bullet_state = "ready"

        if bullet_state is "fire":
            fire_bullet(bulletX, bulletY)
            bulletY -= bulletY_change

        player(playerX, playerY)
        show_score(textX, testY)

        background.update_frame()

        pygame.display.update()

if __name__ == "__main__":
    main()
