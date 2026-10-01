import pygame
import os
import sys
import random
import gif_pygame
os.environ['SDL_VIDEO_WINDOW_POS'] = "%d,%d" % (0,0)

pygame.init()

screenWidth = 1280
screenHeight = 720

screen = pygame.display.set_mode((screenWidth, screenHeight))
pygame.display.set_caption("Epic Space Shooter: Game of the Year Edition")
screen.fill((0, 0, 0))
clock = pygame.time.Clock()

x = 75
bullets = []
enemies = []
bulletIndex = -1
magIndex = 5
playerHealth = 100
playerScore = 0

# Text
arial = pygame.font.SysFont("Arial", 30)
title = arial.render("placeholder text (press r to restart)", False, (0, 0, 0))
ammo = arial.render("Ammo: 5/5", False, (255, 255, 255))
health = arial.render("Health: 100%", False, (255, 255, 255))
score = arial.render("Score: 0", False, (255, 255, 255))

# Bullet
mtndew = pygame.image.load("mountaindew.png").convert_alpha()
dew = pygame.transform.scale(mtndew, (50, 50))
dew_hitbox = dew.get_rect()

# Enemy
dorito = pygame.image.load("dorito.png").convert_alpha()
dor = pygame.transform.scale(dorito, (50, 50))
dorito_hitbox = dor.get_rect()

# Explosion
explosion = gif_pygame.load("Explosion.gif", loops = 1)
s1 = pygame.Surface((48, 48))
s2 = pygame.Surface((48, 48))
s3 = pygame.Surface((48, 48))
s4 = pygame.Surface((48, 48))
s5 = pygame.Surface((48, 48))
s6 = pygame.Surface((48, 48))
s7 = pygame.Surface((48, 48))
s8 = pygame.Surface((48, 48))
s9 = pygame.Surface((48, 48))
s10 = pygame.Surface((48, 48))
s11 = pygame.Surface((48, 48))
s12 = pygame.Surface((48, 48))
s13 = pygame.Surface((48, 48))
s14 = pygame.Surface((48, 48))
s15 = pygame.Surface((48, 48))
explosion_surfs = gif_pygame.GIFPygame([[s1, 0.1], [s2, 0.1], [s3, 0.1], [s4, 0.1], [s5, 0.1], [s6, 0.1], [s7, 0.1], [s8, 0.1], [s9, 0.1], [s10, 0.1], [s11, 0.1], [s12, 0.1], [s13, 0.1], [s14, 0.1], [s15, 0.1]])

# Player Functions
placeholderTexture = pygame.image.load("placeholder.png")
scaledPlaceholder = pygame.transform.scale(placeholderTexture, (50, 20))
placeholder = scaledPlaceholder.get_rect()

def draw_player():
    screen.fill((0, 0, 0))
    placeholder.topleft = (x, 670)

def move_player(direction):
    global x
    if direction == "left":
        if x > 0:
            x -= 8
        else:
            x -= 0
    elif direction == "right":
        if x < 1230:
            x += 8
        else: 
            x += 0

# Bullet class and Functions
class Bullet:
    def __init__(self, name, x, y, image):
        self._name = name
        self._image = image 
        self._rect = image.get_rect()
        self._rect.x = x
        self._rect.y = y
        self._fired = False
    def x(self, x):
        self._rect.x = x
    def get_x(self):
        return self._rect.x
    def y(self, y):
        self._rect.y = y
    def get_y(self):
        return self._rect.y
    def topleft(self, x, y):
        self._rect.topleft = (x, y)
    def check(self):
        return self._fired
    def changeStatus(self, bool):
        self._fired = bool

def create_bullets(bullets):
    for i in range(1, 6):
        new_bullet = Bullet(name = "bullet_" + str(i), x = 1, y = -150, image = dew.copy())
        bullets.append(new_bullet)

def draw_bullet(x, bullets, bulletIndex, magIndex):
    if magIndex >= 0:
        bullets[bulletIndex]._rect.x = x
        bullets[bulletIndex].topleft = (bullets[bulletIndex].get_x(), bullets[bulletIndex].get_y())

        if magIndex >= 0 and bullets[bulletIndex].get_y() <= -150:
            bullets[bulletIndex].y(610)

def update_bullet(i):
    bullets[i]._rect.y = bullets[i].get_y()
    if bullets[i].get_y() > -150:
        bullets[i].y(bullets[i].get_y() - 15)

# Enemy Class and Functions
class Enemy:
    def __init__(self, name, x, y, image):
        self._name = name
        self._image = image 
        self._rect = image.get_rect()
        self._rect.x = x
        self._rect.y = y
        self._alive = False
    def x(self, x):
        self._rect.x = x
    def get_x(self):
        return self._rect.x
    def y(self, y):
        self._rect.y = y
    def get_y(self):
        return self._rect.y
    def topleft(self, x, y):
        self._rect.topleft = (x, y)
    def check(self):
        return self._alive
    def changeStatus(self, bool):
        self._alive = bool

def create_enemies(enemies):
    for i in range(1, 11):
        new_enemy = Enemy(name = "enemy_" + str(i), x = random.randrange(1, 1231), y = -50, image = dor.copy())
        enemies.append(new_enemy)

def draw_enemies():
    i = random.randrange(0, 10)
    enemies[i].changeStatus(True)
    enemies[i].topleft(enemies[i].get_x(), enemies[i].get_y())
    if enemies[i].get_y() >= 720:
        enemies[i].y(-50)
        enemies[i].x(random.randrange(1, 1231))

def update_enemy(i):
    enemies[i]._rect.y = enemies[i].get_y()
    if enemies[i].get_y() < 720:
        enemies[i].y(enemies[i].get_y() + 1.5)

# Collision
def checkEnemyCollision(playerScore):
    for bullet in bullets:
        for enemy in enemies:
            collidedIndex = bullet._rect.colliderect(enemy._rect)
            if collidedIndex:
                screen.blit(explosion_surfs.blit_ready(), (enemy.get_x(), enemy.get_y()))
                enemy.y(800)
                bullet.y(-150)
                playerScore += 10
    return playerScore

def checkPlayerCollision(playerHealth):
    for enemy in enemies:
        collidedIndex = placeholder.colliderect(enemy._rect)
        if collidedIndex:
            enemy.y(800)
            playerHealth -= 34
            return playerHealth
    return playerHealth

runningGame = True
gameOver = False
create_bullets(bullets)
create_enemies(enemies)

pygame.key.set_repeat(400, 400)

# Game Loop
while runningGame:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            runningGame = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                if bulletIndex < 4:
                    bulletIndex += 1
                elif bulletIndex == 4:
                    bulletIndex = 0
                
                magIndex -= 1
                if magIndex >= 0:
                    ammo = arial.render("Ammo: "+str(magIndex)+"/5", False, (255, 255, 255))
                draw_bullet(x, bullets, bulletIndex, magIndex)
            if event.key == pygame.K_r:
                if magIndex != 5:
                    magIndex = 5
                    ammo = arial.render("Ammo: 5/5", False, (255, 255, 255))

    pressed = pygame.key.get_pressed()
    if pressed[pygame.K_a]:
        move_player("left")
    if pressed[pygame.K_d]:
        move_player("right")

    draw_player()
    screen.blit(scaledPlaceholder, placeholder)
    playerHealth = checkPlayerCollision(playerHealth)
    health = arial.render("Health: "+str(playerHealth)+"%", False, (255, 255, 255))
    if playerHealth <= 0:
        runningGame = False
        gameOver = True

    i = 0
    for i in range(len(bullets)):
        if bullets[i].check:
            update_bullet(i)

    for i in range(len(bullets)):
        screen.blit(bullets[i]._image, bullets[i]._rect)

    rand = random.randrange(0, 10)
    if rand == 1: 
        draw_enemies()

    for i in range(len(enemies)):
        if enemies[i].check():
            update_enemy(i)

    for i in range(len(enemies)):
        screen.blit(enemies[i]._image, enemies[i]._rect)

    playerScore = checkEnemyCollision(playerScore)
    score = arial.render("Score: "+str(playerScore)+"", False, (255, 255, 255))

    screen.blit(ammo, (1, 1))
    screen.blit(health, (1, 25))
    screen.blit(score, (1, 50))

    # explodeX, explodeY, boom = checkEnemyCollision(explosion)
    # if boom:
    #     screen.blit(explosion.blit_ready(), (explodeX, explodeY))
    #     if explosion.frame == len(explosion.get_surfaces()) - 1:
    #         boom = False

    pygame.display.update()
    clock.tick(60)

while gameOver:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            gameOver = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_r:
                runningGame = True
                gameOver = False

    screen.fill((255, 255, 255))
    screen.blit(title, (550, 300))
    pygame.display.update()

if runningGame == False and gameOver == False:
    pygame.quit()
    quit()