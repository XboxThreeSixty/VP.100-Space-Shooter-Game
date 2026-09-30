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

# Text
arial = pygame.font.SysFont("Arial", 30)
title = arial.render("placeholder text", False, (0, 0, 0))
# screen.blit(title, (0, 0)) prints the text onto the screen; the 2 numbers are x and y values. This will be used for a future title screen.

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

# Player Functions
def draw_player():
    screen.fill((0, 0, 0))
    pygame.draw.rect(screen, (255, 0, 0), [x, 670, 50, 20], 0)

def move_player(direction):
    global x
    if direction == "left":
        if x > 0:
            x -= 5
        else:
            x -= 0
    elif direction == "right":
        if x < 1230:
            x += 5
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
    print("Magazine: 5/5 bullets")

def draw_bullet(x, bullets, bulletIndex, magIndex):
    if magIndex >= 0:
        bullets[bulletIndex]._rect.x = x
        bullets[bulletIndex].topleft = (bullets[bulletIndex].get_x(), bullets[bulletIndex].get_y())
        print("Magazine: "+str(magIndex)+"/5 bullets")

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
def checkEnemyCollision():
    for bullet in bullets:
        for enemy in enemies:
            collidedIndex = bullet._rect.colliderect(enemy._rect)
            if collidedIndex:
                enemy.y(800)
                bullet.y(-150)
                return enemy.get_x(), enemy.get_y(), True
    return 0, 0, False

runningGame = True
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
                draw_bullet(x, bullets, bulletIndex, magIndex)
            if event.key == pygame.K_r:
                if magIndex != 5:
                    magIndex = 5
                    print("\nMagazine: 5/5 bullets")

    pressed = pygame.key.get_pressed()
    if pressed[pygame.K_a]:
        move_player("left")
    if pressed[pygame.K_d]:
        move_player("right")

    draw_player()
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

    explodeX, explodeY, boom = checkEnemyCollision()
    if boom:
        screen.blit(explosion.blit_ready(), (100, 100))
        if explosion.frame == len(explosion.get_surfaces()) - 1:
            boom = False

    pygame.display.update()
    clock.tick(60)

pygame.quit()
quit()