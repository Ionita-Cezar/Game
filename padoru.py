import pygame
import math
import random
from pygame import mixer

# Initialize the pygame
pygame.init()

# Create the screen
screen = pygame.display.set_mode((800, 600))

# Background
background = pygame.image.load('assets/background.png')

# Background sound
mixer.music.load('assets/padoru-bgm.wav')
mixer.music.play(-1)

# Title and Icon
pygame.display.set_caption('Padoru')
icon = pygame.image.load('assets/padoru.png')
pygame.display.set_icon(icon)

# PLayer
playerImg = pygame.image.load('assets/player.png')
playerX = 100
playerY = 250
playerX_change = 0
playerY_change = 0

# Enemy
moonImg = []
moonX = []
moonY = []
moonX_change = []
moonY_change = []
num_of_moon = 3

for i in range(num_of_moon):
    moonImg.append(pygame.image.load('assets/moon.png'))
    moonX.append(random.randint(800, 900))
    moonY.append(random.randint(10, 540))
    moonX_change.append(0)
    moonY_change.append(0)

# Bullet
presentImg = pygame.image.load('assets/present.png')
presentX = 0
presentY = 0
presentX_change = 0.8
presentY_change = 0
present_state = 'ready'

# Score
score_value = 0
font = pygame.font.Font('freesansbold.ttf', 32)
textX = 10
textY = 10


def show_score(x, y):
    score = font.render('Score : ' + str(score_value), True, (255, 0, 0))
    screen.blit(score, (x, y))


def game_over_effects():
    over_font = pygame.font.Font('freesansbold.ttf', 64)
    #game_over_sound = mixer.Sound('assets/game-over.wav')
    over_text = over_font.render('GAME OVER', True, (255, 0, 0))
    screen.blit(over_text, (200, 250))
    #game_over_sound.play()
    #game_over_sound.stop()


def player(x, y):
    screen.blit(playerImg, (x, y))


def moon(x, y, i):
    screen.blit(moonImg[i], (x, y))


def fire_present(x, y):
    global present_state
    present_state = 'fire'
    screen.blit(presentImg, (x + 10, y + 20))


def Collision(moonX, moonY, presentX, presentY):
    distance = math.sqrt((math.pow(moonX - presentX, 2)) + (math.pow(moonY - presentY, 2)))
    if distance < 27:
        return True
    else:
        return False


mode = 'game'

# Game loop
running = True
while running:
    if mode == 'game':

        # Background image
        screen.blit(background, (0, 0))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            # Player movement
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT or event.key == ord('a'):
                    playerX_change = -0.3
                if event.key == pygame.K_RIGHT or event.key == ord('d'):
                    playerX_change = 0.3
                if event.key == pygame.K_UP or event.key == ord('w'):
                    playerY_change = -0.3
                if event.key == pygame.K_DOWN or event.key == ord('s'):
                    playerY_change = 0.3

                if event.key == pygame.K_ESCAPE:
                    running = False

                if event.key == pygame.K_SPACE:
                    if present_state == 'ready':
                        present_sound = mixer.Sound('assets/shooting.wav')
                        present_sound.play()
                        presentX = playerX
                        presentY = playerY
                        fire_present(presentX, presentY)

            if event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT or event.key == ord('a') \
                        or event.key == pygame.K_RIGHT or event.key == ord('d'):
                    playerX_change = 0
                if event.key == pygame.K_UP or event.key == ord('w') \
                        or event.key == pygame.K_DOWN or event.key == ord('s'):
                    playerY_change = 0

        playerX += playerX_change
        playerY += playerY_change

        # Boundries
        if playerX <= 0:
            playerX = 0
        elif playerX >= 300:
            playerX = 300
        if playerY <= 0:
            playerY = 0
        elif playerY >= 535:
            playerY = 535

        # Enemy
        for i in range(num_of_moon):

            # Game Over
            player_collision = Collision(moonX[i], moonY[i], playerX, playerY)
            if player_collision or moonX[i] < 0:
                mode = 'game over'
                break

            # Enemy movement
            moonX[i] += moonX_change[i]

            if moonX[i] >= 0:
                moonX_change[i] = -0.2

            # Collision
            present_collision = Collision(moonX[i], moonY[i], presentX, presentY)
            if present_collision:
                collision_sound = mixer.Sound('assets/collision.wav')
                collision_sound.play()
                presentX = playerX
                presentY = playerY
                present_state = 'ready'
                score_value += 1
                moonX[i] = random.randint(800, 900)
                moonY[i] = random.randint(10, 540)

            moon(moonX[i], moonY[i], i)

        # Bullet movement
        if presentX >= 800:
            presentX = playerX
            present_state = 'ready'

        if present_state == 'fire':
            fire_present(presentX, presentY)
            presentX += presentX_change

        player(playerX, playerY)
        show_score(textX, textY)
        pygame.display.update()

    elif mode == 'game over':
        # Screen color
        screen.fill((0, 0, 0))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        game_over_effects()

        pygame.display.update()
