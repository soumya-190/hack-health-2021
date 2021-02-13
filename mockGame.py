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
mixer.music.load("UI/game/background.wav")
mixer.music.play(-1)

# Caption and Icon
pygame.display.set_caption("Hack Health")
icon = pygame.image.load('UI/sprites/face.png')
pygame.display.set_icon(icon)

# Player
playerImg = pygame.image.load('UI/sprites/kid_idle.png')
playerX = 370
playerY = 480
playerX_change = 0

# Enemy
enemyImg = []
enemyX = []
enemyY = []
enemyX_change = []
enemyY_change = []
num_of_enemies = 8

for i in range(num_of_enemies):
    enemyImg.append(pygame.image.load('UI/sprites/karen_left.png'))
    enemyX.append(random.randint(0, 736))
    enemyY.append(random.randint(50, 150))
    enemyX_change.append(20)
    enemyY_change.append(50)

# Masks
maskImg = []
maskX = []
maskY = []
maskY_change = []
num_of_mask = 8

for i in range(num_of_mask):
    maskImg.append(pygame.image.load('UI/sprites/mask.png'))
    maskX.append(random.randint(0, 736))
    maskY.append(random.randint(50, 150))
    maskY_change.append(50)


# Bullet

# Ready - You can't see the bullet on the screen
# Fire - The bullet is currently moving

bulletImg = pygame.image.load('UI/sprites/sanitizer.png')
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


def enemy(x, y, i):
    screen.blit(enemyImg[i], (x, y))

def mask(x, y, i):
    screen.blit(maskImg[i], (x, y))

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

if __name__ == "__main__":
    
    # Game Loop
    running = True
    while running:

        # RGB = Red, Green, Blue
        screen.fill((0, 0, 0))

        # Background Image
        screen.blit(background, (0, 0))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            # if keystroke is pressed check whether its right or left
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    playerX_change = -5
                if event.key == pygame.K_RIGHT:
                    playerX_change = 5
                if event.key == pygame.K_SPACE:
                    if bullet_state is "ready":
                        bulletSound = mixer.Sound("UI/game/laser.wav")
                        bulletSound.play()
                        # Get the current x cordinate of the spaceship
                        bulletX = playerX
                        fire_bullet(bulletX, bulletY)

            if event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                    playerX_change = 0

        playerX += playerX_change
        if playerX <= 0:
            playerX = 0
        elif playerX >= 736:
            playerX = 736

        # Enemy Movement
        for i in range(num_of_enemies):

            # Game Over
            #print("line 158 enemyY[{}] = {}".format(i, enemyY[i]))
            #print("line 158 playerY = {}".format(playerY))
            print(enemyY)

            if enemyY[i] >= playerY:
                for j in range(num_of_enemies):
                    enemyY[j] = 2000
                game_over_text()
                break

            enemyX[i] += enemyX_change[i]
            if enemyX[i] <= 0:
                enemyX_change[i] = 4
                enemyY[i] += enemyY_change[i]
                print("line 169 enemyY[{}] changed to {}".format(i, enemyY[i]))
            elif enemyX[i] >= 736:
                # Flip everything to the display
                pygame.display.flip()
                # Ensure program maintains a rate of 30 frames per second
                clock.tick(60)
                enemyX_change[i] = -4
                enemyY[i] += enemyY_change[i]
                print("line 173 enemyY[{}] changed to {}".format(i, enemyY[i]))

            # Collision
            collision = isCollision(enemyX[i], enemyY[i], bulletX, bulletY)
            if collision:
                explosionSound = mixer.Sound("UI/game/explosion.wav")
                explosionSound.play()
                bulletY = 480
                bullet_state = "ready"
                score_value += 1
                enemyX[i] = random.randint(0, 736)
                enemyY[i] = random.randint(50, 150)
                print("line 185 enemyY[{}] changed to {}".format(i, enemyY[i]))

            enemy(enemyX[i], enemyY[i], i)
            mask(maskX[i], maskY[i], i)

        # Bullet Movement
        if bulletY <= 0:
            bulletY = 480
            bullet_state = "ready"

        if bullet_state is "fire":
            fire_bullet(bulletX, bulletY)
            bulletY -= bulletY_change

        player(playerX, playerY)
        show_score(textX, testY)
        pygame.display.update()
