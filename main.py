import pygame as py
import random as rd
import math as math
from pygame import mixer
# initializing the pygame
py.init()

# screen
screen = py.display.set_mode((800, 600))

# background
background = py.image.load('background.png')
mixer.music.load('background.wav')
mixer.music.play(-1)  # -1 so that it plays forever

# title and logo
py.display.set_caption("Spaceship Battles")
icon = py.image.load('spaceship.png')
py.display.set_icon(icon)

# Player
playerImg = py.image.load('player.png')
player_x = 370
player_y = 480
player_x_change = 0

# Enemy
enemyImg = []
enemy_x = []
enemy_y = []
enemy_x_change = []
enemy_y_change = []
no_of_enemy = 7
for i in range(no_of_enemy):
    enemyImg.append(py.image.load('enemy.png'))
    # because we want the enemy in different places every time
    enemy_x.append(rd.randint(0, 780))
    enemy_y.append(rd.randint(50, 150))
    # to keep moving the enemy even if the value is not 0
    enemy_x_change.append(2.5)
    enemy_y_change.append(30)

# bullet
# ready - bullet is not visible on the screen
# fired - bullet is visible
bulletImg = py.image.load('bullet.png')
bullet_x = 0
bullet_y = 480  # bullet position = player position
bullet_x_change = 0
bullet_y_change = 6
bullet_state = "ready"

# detecting collision
def is_collision(enemy_x, enemy_y, bullet_x, bullet_y):
    distance = math.sqrt((math.pow(enemy_x-bullet_x, 2)) +
                         (math.pow(enemy_y-bullet_y, 2)))  # distance formula
    if distance < 37:
        return True
    else:
        return False


# score
score_value = 0
font = py.font.Font('freesansbold.ttf', 32)
score_x = 10
score_y = 10


def show_score(x, y):
    score = font.render("Score:" + str(score_value), True, (255, 255, 255))
    screen.blit(score, (x, y))

#game over
def game_over():
    over_font = py.font.Font('freesansbold.ttf', 64)
    over = over_font.render("Game Over" , True, (255, 255, 255))
    screen.blit(over, (250,270))



# if collision occur
def collision_true():
    global bullet_y, bullet_state, enemy_x, enemy_y, score_value, i
    bullet_y = 480
    bullet_state = "ready"
    score_value += 1
    enemy_x[i] = rd.randint(0, 780)
    enemy_y[i] = rd.randint(50, 170)


def player(x, y):
    screen.blit(playerImg, (x, y))


def enemy(x, y, i):
    screen.blit(enemyImg[i], (x, y))


def fire_bullet(x, y):
    global bullet_state
    bullet_state = "fired"
    # because we want the bullets to be shooted from the nose of spaceship
    screen.blit(bulletImg, (x+16, y+10))


# Game loop
if __name__ == '__main__':
    running = True
    while running:
        for event in py.event.get():
            if event.type == py.QUIT:  # when we press the cross button
                running = False  # while loop becomes False and gets terminated
                # until then the screen remains visible

            if event.type == py.KEYDOWN:  # checking if any key is pressed or not
                if event.key == py.K_LEFT:  # if left key is pressed
                    player_x_change = -3.5

                if event.key == py.K_RIGHT:  # if right key is pressed
                    player_x_change = 3.5

                if event.key == py.K_SPACE:
                    # if bullet is not on screen then only shoot another bullet.
                    if bullet_state == "ready":
                        bullet_sound = mixer.Sound('bullet.wav')
                        bullet_sound.play()
                        # when we press space then the currrent value of player_x is stored in bullet_x
                        # so after firing it will not follow the player
                        bullet_x = player_x
                        fire_bullet(bullet_x, bullet_y)

            if event.type == py.KEYUP:  # when key is released
                if event.key == py.K_LEFT or event.key == py.K_RIGHT:
                    player_x_change = 0
        player_x += player_x_change

        # setting background color
        screen.fill((0, 0, 0))

        # background image
        screen.blit(background, (0, 0))

        # adding bounudaries
        if player_x <= 0:
            player_x = 0
        elif player_x >= 736:
            player_x = 736

        # enemy movement
        for i in range(no_of_enemy):
            #game over
            if enemy_y[i]>410:
                for j in range(no_of_enemy):
                    enemy_y[j] = 2000
                game_over()
                over_sound = mixer.Sound('gameover.wav')
                over_sound.play()
                break
            enemy_x[i] += enemy_x_change[i]
            if enemy_x[i] <= 0:
                enemy_x_change[i] = 2.5
                enemy_y[i] += enemy_y_change[i]
            elif enemy_x[i] >= 736:
                enemy_x_change[i] = -2.5
                enemy_y[i] += enemy_y_change[i]

            # collision detection
            collision = is_collision(
                enemy_x[i], enemy_y[i], bullet_x, bullet_y)
            if collision is True:
                explosion = mixer.Sound('explosion.wav')
                explosion.play()
                collision_true()
            enemy(enemy_x[i], enemy_y[i], i)

        # bullet movement
        if bullet_y <= 0:
            bullet_y = 480
            bullet_state = "ready"
        if bullet_state == "fired":
            fire_bullet(bullet_x, bullet_y)
            bullet_y -= bullet_y_change

        player(player_x, player_y)
        show_score(score_x, score_y)
        py.display.update()  # to update the changes
