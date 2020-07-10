import pygame
import random
import math
import sys

#  initialization
pygame.init()

# create the screen width, length()
screen = pygame.display.set_mode((1280, 720))
screen_color = (0, 0, 0)

# font style, size and color for text
small_font = pygame.font.SysFont('Corbel', 30)
color = (255, 255, 255)

# title of the window
pygame.display.set_caption('Space Invader')

# icon of the window
icon = pygame.image.load('uni.png')
pygame.display.set_icon(icon)

# Player
playerImg = pygame.image.load('spaceship.png')
playerX = random.randint(0, 1216)
playerY = 590
playerX_change = 0
player_score = 0
player_lives = 2

# Enemy
enemyImg = []
enemyX = []
enemyY = []
enemyX_change = []
enemyY_change = []
num_of_enemies = 6

# background image
bgImg = pygame.image.load('2352hd.jpg')

# bullet image
bulletImg = pygame.image.load('bullet.png')
bulletX = 0
bulletY = 600
bulletX_change = 0
bulletY_change = 0
bullet_state = "ready"

# start screen, game over screen, quit, play again options
start = pygame.image.load('start.png')
startY = 0
startY_change = 0
start_game_ = small_font.render("Press P to Start Game", True, color)
z = 620
z_change = 0
game_over = pygame.image.load("gameOver.png")
quit_ = small_font.render('Press Q to quit game', True, color)
replay = small_font.render('Press R to play again', True, color)
game_started = False


def start_game(y):
    screen.blit(start, (0, y))


def play(y):
    screen.blit(start_game_, (490, y))


def player(x, y):
    screen.blit(playerImg, (x, y))


def enemy(x, y, a):
    screen.blit(enemyImg[a], (x, y))


def bullet(x, y):
    screen.blit(bulletImg, (x, y))


def is_collision(a, b, c, d):
    distance = math.sqrt((math.pow(a - b, 2)) + (math.pow(c - d, 2)))
    if distance < 35:
        return True
    else:
        return False


def player_enemy_collision(a, b, c, d):
    distance = math.sqrt((math.pow(a - b, 2)) + (math.pow(c - d, 2)))
    if distance < 57:
        return True
    else:
        return False


def game_overs():
    global player_lives
    if player_lives <= 0:
        return True
    else:
        return False


# loop to make the window continuously be shown
running = True

while running:

    score = small_font.render('Score - ' + str(player_score), True, color)
    lives = small_font.render('Lives Left - ' + str(player_lives), True, color)

    # display background color
    screen.fill(screen_color)
    screen.blit(bgImg, (0, 0))
    screen.blit(score, (10, 20))
    screen.blit(lives, (1100, 20))

    for i in range(num_of_enemies):
        enemyImg.append(pygame.image.load('alien.png'))
        enemyX.append(random.randint(0, 1216))
        enemyY.append(random.randint(50, 150))
        enemyX_change.append(5)
        enemyY_change.append(60)

    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_p and not game_started:
                startY_change -= 40
                z_change += 20
                game_started = True

            elif event.key == pygame.K_r and not game_started:
                player_lives = 2
                score = 0
                num_of_enemies = 6
                game_started = True

                for i in range(num_of_enemies):
                    enemyX[i] = random.randint(0, 1216)
                    enemyY[i] = random.randint(0, 150)
                playerX = random.randint(0, 1216)

            elif event.key == pygame.K_q and not game_started:
                running = False

            if event.key == pygame.K_LEFT:
                playerX_change -= 5
                if bullet_state == 'ready:':
                    bulletX_change -= 5

            elif event.key == pygame.K_RIGHT:
                playerX_change += 5
                if bullet_state == 'ready:':
                    bulletX_change += 5

            elif event.key == pygame.K_SPACE and bullet_state == "ready":
                if bullet_state == "ready":
                    bulletY_change = 30
                    bulletX = playerX
                    bullet_state = "fired"

            elif event.key == pygame.K_MINUS:
                player_lives -= 1

            elif event.key == pygame.K_EQUALS:
                player_lives += 1

            elif event.key == pygame.K_d and game_started:
                num_of_enemies -= 1

            elif event.key == pygame.K_s and game_started:
                num_of_enemies += 1

        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                playerX_change = 0

    # movement
    playerX += playerX_change

    # border
    if playerX <= 0:
        playerX = 0
    elif playerX >= 1216:
        playerX = 1216

    # enemy movement

    for i in range(num_of_enemies):
        enemyX[i] += enemyX_change[i]
        if enemyX[i] <= 0:
            enemyX_change[i] = 10
            enemyY[i] += enemyY_change[i]

        elif enemyX[i] >= 1216:
            enemyX_change[i] = -10
            enemyY[i] += enemyY_change[i]

        elif enemyY[i] >= 700:
            enemyX[i] = random.randint(0, 1216)
            enemyY[i] = random.randint(50, 150)

        # collision
        collision = is_collision(enemyX[i], bulletX, enemyY[i], bulletY)

        if collision:
            enemyX[i] = random.randint(0, 1216)
            enemyY[i] = random.randint(50, 150)
            bullet_state = "ready"
            bulletX = playerX
            bulletY = 590
            bulletY_change = 0
            player_score += 1

        player_enemy_col = player_enemy_collision(enemyX[i], playerX, enemyY[i], playerY)

        if player_enemy_col:
            enemyX[i] = random.randint(0, 1216)
            enemyY[i] = random.randint(50, 150)
            playerX = random.randint(0, 1216)
            playerY = 590
            bullet_state = "ready"
            bulletX = playerX
            bulletY = 590
            bulletY_change = 0
            player_lives -= 1

        enemy(enemyX[i], enemyY[i], i)

    bulletX += bulletX_change
    bullet(bulletX + 16, bulletY)
    player(playerX, playerY)

    # bullet movement
    if bulletY <= 0:
        bulletY = 590
        bulletY_change = 0
        bullet_state = "ready"

    if bullet_state == "ready":
        bulletX = playerX

    bulletY -= bulletY_change

    # game over
    game_over_ = game_overs()

    if game_over_:
        screen.blit(game_over, (0, 0))
        screen.blit(quit_, (790, 620))
        screen.blit(replay, (190, 620))
        game_started = False

    startY += startY_change
    z += z_change
    start_game(startY)
    play(z)

    if startY <= -720 and z >= 720:
        startY_change = 0
        z_change = 0

    # to update the display continuously
    pygame.display.update()
