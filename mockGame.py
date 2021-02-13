import math
import random

import pygame
from pygame import mixer

# Setup the clock for a decent framerate
clock = pygame.time.Clock()

# Intialize the pygame
pygame.init()

# create the screen
screen = pygame.display.set_mode((800, 600))

# Background
background = pygame.image.load('UI/sprites/background.png')

# Sound
#mixer.music.load("UI/game/background.wav")
mixer.music.play(-1)

# Caption and Icon
pygame.display.set_caption("Hack Health")
icon = pygame.image.load('UI/sprites/face.png')
pygame.display.set_icon(icon)

class Player:
    frame = 0
    maxframe = 4
    bufferi = 0
    buffer = 10
    frames = [pygame.image.load('UI/sprites/kid_idle.png'), pygame.image.load("UI/sprites/kid_left.png"),pygame.image.load("UI/sprites/kid_idle.png"), pygame.image.load("UI/sprites/kid_right.png")]
    dam_frames = [pygame.image.load("UI/sprites/kid_damage.png"), pygame.image.load("UI/sprites/kid_left_dam.png"),pygame.image.load("UI/sprites/kid_damage.png"), pygame.image.load("UI/sprites/kid_right_dam.png")]
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
    frames = [pygame.image.load("UI/sprites/karen_left.png"), pygame.image.load("UI/sprites/karen_right.png")]
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
    frames = [pygame.image.load("UI/sprites/background.png"), pygame.image.load("UI/sprites/background.png"),pygame.image.load("UI/sprites/background.png"),pygame.image.load("UI/sprites/background.png"),pygame.image.load("UI/sprites/background.png"), pygame.image.load("UI/sprites/background.png"), pygame.image.load("UI/sprites/background.png")]

    def getframe(self):
        return self.frame

    def update_frame(self):
        self.bufferi += 1
        if self.bufferi == self.buffer:
            self.frame += 1
            self.bufferi = 0
            if self.frame == self.maxframe:
                self.frame = 0

# Player
playerImg = pygame.image.load('UI/sprites/kid_idle.png')
playerX = 370
playerY = 480
playerX_change = 0

# Other people on screen
karenImg = []
karenX = []
karenY = []
karenX_change = []
karenY_change = []
num_of_karens = 8

for i in range(num_of_karens):
    karenImg.append(pygame.image.load('UI/sprites/karen_left.png'))
    karenX.append(random.randint(0, 736))
    karenY.append(random.randint(50, 150))
    karenX_change.append(20)
    karenY_change.append(50)

# Masks
maskImg = []
maskX = []
maskY = []
maskY_change = []
num_of_masks = 8

for i in range(num_of_masks):
    maskImg.append(pygame.image.load('UI/sprites/mask.png'))
    maskX.append(random.randint(0, 736))
    maskY.append(random.randint(50, 150))
    maskY_change.append(50)

# Hand Sanitizer
sanitizerImg = pygame.image.load('UI/sprites/sanitizer.png')
sanitizerX = 0
sanitizerY = 480
sanitizerX_change = 0
sanitizerY_change = 10
sanitizer_state = "ready"

# Score
score_value = 0
font = pygame.font.Font('freesansbold.ttf', 32)

textX = 10
testY = 10

# Game Over
over_font = pygame.font.Font('freesansbold.ttf', 64)

# change position of enemy once reaches boundary
def bounce(x, y):
    if x > 440:
        x = 2 * (440) - x
    elif x < 0:
        x = 2 * (0) - x
    if y > 150:
        y = 2 * (150) - y
    elif y < 50:
        y = 2 * (50) - y
    return (x, y)

def show_score(x, y):
    score = font.render("Score : " + str(score_value), True, (255, 255, 255))
    screen.blit(score, (x, y))


def game_over_text():
    over_text = over_font.render("GAME OVER", True, (255, 255, 255))
    screen.blit(over_text, (200, 250))


def player(x, y):
    screen.blit(playerImg, (x, y))


def karen(x, y, i):
    screen.blit(karenImg[i], (x, y))

def mask(x, y, i):
    screen.blit(maskImg[i], (x, y))

def fire_sanitizer(x, y):
    global sanitizer_state
    sanitizer_state = "fire"
    screen.blit(sanitizerImg, (x + 16, y + 10))

def isCollision(karenX, karenY, sanitizerX, sanitizerY):
    distance = math.sqrt(math.pow(karenX - sanitizerX, 2) + (math.pow(karenY - sanitizerY, 2)))
    if distance < 27:
        return True
    else:
        return False

if __name__ == "__main__":
    
    # Game Loop
    running = True
    while running:
        screen.fill((0, 0, 0))
        screen.blit(background, (0, 0))

        # Check pygame events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False #Stop the game

            
            if event.type == pygame.KEYDOWN:

                #left key moves player left
                if event.key == pygame.K_LEFT: 
                    playerX_change = -5

                #right key moves player right
                if event.key == pygame.K_RIGHT: 
                    playerX_change = 5
                
                #space bar send hand sanitizer
                if event.key == pygame.K_SPACE: 

                    #Check bullet is not already fired
                    if sanitizer_state is "ready":
                        sanitizerSound = mixer.Sound("UI/game/laser.wav")
                        sanitizerSound.play()

                        # Get the current x cordinate of the player
                        sanitizerX = playerX
                        fire_sanitizer(sanitizerX, sanitizerY)

            # Only moves player when button is pressed (player stops moving when button not pressed)
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                    playerX_change = 0

        playerX += playerX_change
        if playerX <= 0:
            playerX = 0
        elif playerX >= 736:
            playerX = 736

        # Enemy Movement
        for i in range(num_of_karens):

            if playerX_change != 0 and screen.get_at(player.peek_next()) != background:
                game_over_text()
                break

            print(karenY)
            # Game over when enemy touches player
            if karenY[i] >= 440 and karenX[i] >= 0:
                print(karenY[i], karenX[i])
                for j in range(num_of_karens):
                    karenY[j] = 2000
                game_over_text()

            # Change enemy x position
            karenX[i] += karenX_change[i]

            #Set x change to positive number if < 0
            if karenX[i] <= 0:
                karenX_change[i] = 4 
                karenY[i] += karenY_change[i]
                #print("line 169 enemyY[{}] changed to {}".format(i, enemyY[i]))
            
            #Set x change to smaller number if > 736
            elif karenX[i] >= 736:
                karenX_change[i] = -4
                karenY[i] += karenY_change[i]
                #print("line 173 enemyY[{}] changed to {}".format(i, enemyY[i]))

            # Check hand sanitizer collided with enemy
            collision = isCollision(karenX[i], karenY[i], sanitizerX, sanitizerY)
            if collision:
                explosionSound = mixer.Sound("UI/game/explosion.wav")
                explosionSound.play()
                sanitizerY = 480
                sanitizer_state = "ready"
                score_value += 1
                karenX[i] = random.randint(0, 736)
                karenY[i] = random.randint(50, 150)
                print("line 185 enemyY[{}] changed to {}".format(i, karenY[i]))

            karen(karenX[i], karenY[i], i)
            mask(maskX[i], maskY[i], i)

        # Bullet Movement
        if sanitizerY <= 0:
            sanitizerY = 480
            sanitizer_state = "ready"

        if sanitizer_state is "fire":
            fire_sanitizer(sanitizerX, sanitizerY)
            sanitizerY -= sanitizerY_change

        player(playerX, playerY)
        show_score(textX, testY)
        pygame.display.update()
