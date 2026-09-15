import pygame
import os
os.environ['SDL_VIDEO_WINDOW_POS'] = "%d,%d" % (0,0)

pygame.init()

screenWidth = 1280
screenHeight = 720

screen = pygame.display.set_mode((screenWidth, screenHeight))
pygame.display.set_caption("Basic Space Shooter")
screen.fill((0, 0, 0))
clock = pygame.time.Clock()

x = 75
bullet_y = 490
bullets = []

mtndew = pygame.image.load("mountaindew.png").convert_alpha()
dew = pygame.transform.scale(mtndew, (50, 50))
dew_hitbox = dew.get_rect()
# dew_hitbox.topleft = (150, 100)

# Functions
def draw_player():
    screen.fill((0, 0, 0))
    pygame.draw.rect(screen, (255, 0, 0), [x, 550, 50, 20], 0)

def move_player(direction):
    global x
    if direction == "left":
        if x > 0:
            x -= 3
        else:
            x -= 0
    elif direction == "right":
        if x < 1230:
            x += 3
        else: 
            x += 0

class Bullet:
    def __init__(self, name):
        self.name = name

def create_bullets():
    global bullets
    i = 0
    for i in range(1, 6):
        new_bullet = Bullet(name = "bullet_" + str(i))
        bullets.append(new_bullet)

def draw_bullet():
    global x
    global bullet_y
    dew_hitbox.topleft = (x, bullet_y)

def update_bullet():
    global x
    global bullet_y
    if bullet_y > -50:
        bullet_y -= 5

gameFlag = True
create_bullets()

# Game Loop
while gameFlag:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            gameFlag = False

    pressed = pygame.key.get_pressed()
    if pressed[pygame.K_a]:
        move_player("left")
    if pressed[pygame.K_d]:
        move_player("right")
    if pressed[pygame.K_SPACE]:
        draw_bullet()
    if pressed[pygame.K_r]:
        pass

    draw_player()
    update_bullet()

    screen.blit(dew, dew_hitbox)

    pygame.display.update()
    clock.tick(60)

pygame.quit()
quit()