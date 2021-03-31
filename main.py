import pygame
from pygame import mixer
import random
import math


# Intialize the pygame
pygame.init()

# intialize the font
pygame.font.init()

# create the screen
width, height = 800, 600
screen = pygame.display.set_mode((width, height))

# Background
background = pygame.transform.scale(pygame.image.load('background.png'), (width, height))

#background sound
mixer.music.load('background.wav')
mixer.music.play(-1)

# Caption and Icon
pygame.display.set_caption("Alien Invaders")
icon = pygame.image.load('ufo.png')
pygame.display.set_icon(icon)

# Player and location
playerImg = pygame.image.load('player.png')
playerX = 370
playerY = 480
playerX_change = 0

enemy_img = []
enemyX = []
enemyY = []
enemyX_change = []
enemyY_change = []
num_of_enemies = 5

# enemy and location
for i in range(num_of_enemies):
    enemy_img.append(pygame.image.load('enemy.png'))
    enemyX.append(random.randint(0, 736))
    enemyY.append(random.randint(20, 150))
    enemyX_change.append(5)
    enemyY_change.append(30)

# laser and location
laser_img = pygame.image.load('bullet.png')
laserX = 0
laserY = 480
laserX_change = 0
laserY_change = 10
laser_condition = "ready"

# Score

score = 0
font = pygame.font.SysFont('comicsans', 32)

textX = 10
textY = 10

# Game Over
over_font = pygame.font.SysFont('freesansbold.ttf', 100)


def show_score(x, y):
    score_value = font.render("Score : " + str(score), True, (255, 255, 255))
    screen.blit(score_value, (x, y))


def game_over_text():
    over_text = over_font.render("GAME OVER", True, (255, 255, 255))
    screen.blit(over_text, (200, 250))


def show_score(x, y):
    score_value = font.render("SCORE :" + str(score), True, (255, 255, 255))
    screen.blit(score_value, (x, y))


def isCollision(enemyX, enemyY, bulletX, bulletY):
    distance = math.sqrt(math.pow(enemyX - bulletX, 2) + (math.pow(enemyY - bulletY, 2)))
    if distance < 27:
        return True
    else:
        return False


def player(x, y):
    screen.blit(playerImg, (x, y))


def enemy(x, y, i):
    screen.blit(enemy_img[i], (x, y))


def laser_fire(x, y):
    global laser_condition
    laser_condition = "fire"
    screen.blit(laser_img, (x + 16, y + 10))


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
                if laser_condition == "ready":
                    laser_sound = mixer.Sound('laser.wav')
                    laser_sound.play()

                    laserX = playerX
                    laser_fire(laserX, laserY)

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                playerX_change = 0

    playerX += playerX_change
    if playerX <= 0:
        playerX = 0
    elif playerX >= 736:
        playerX = 736

    # enemy movement
    for i in range(num_of_enemies):

        # game over
        if enemyY[i] > 420:
            for j in range(num_of_enemies):
                enemyY[i] = 3000
            game_over_text()
            break

        enemyX[i] += enemyX_change[i]
        if enemyX[i] <= 0:
            enemyX_change[i] = 1
            enemyY[i] += enemyY_change[i]
        elif enemyX[i] >= 736:
            enemyX_change[i] = -1
            enemyY[i] += enemyY_change[i]

        # Collision
        collision = isCollision(enemyX[i], enemyY[i], laserX, laserY)
        if collision:
            collision_sound = mixer.Sound('explosion.wav')
            collision_sound.play()
            bulletY = 480
            bullet_state = "ready"
            score += 1
            enemyX[i] = random.randint(0, 736)
            enemyY[i] = random.randint(50, 150)

        enemy(enemyX[i], enemyY[i], i)

    # laser movement
    if laserY <= 20:
        laserY = 480
        laser_condition = "ready"
    if laser_condition == "fire":
        laser_fire(laserX, laserY)
        laserY -= laserY_change

    player(playerX, playerY)
    show_score(textX, textY)
    pygame.display.update()
