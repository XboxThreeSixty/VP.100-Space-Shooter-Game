import pygame
import os
os.environ['SDL_VIDEO_WINDOW_POS'] = "%d,%d" % (0,0)

pygame.init()

screenWidth = 1280
screenHeight = 720

screen = pygame.display.set_mode((screenWidth, screenHeight))
pygame.display.set_caption("Epic Space Shooter: Game of the Year Edition")
screen.fill((0, 0, 0))
clock = pygame.time.Clock()

x = 75
bullet_y = 610
bullets = []
bulletOnScreen = False

mtndew = pygame.image.load("mountaindew.png").convert_alpha()
dew = pygame.transform.scale(mtndew, (50, 50))
dew_hitbox = dew.get_rect()
# dew_hitbox.topleft = (150, 100)

# Functions
def draw_player():
    screen.fill((0, 0, 0))
    pygame.draw.rect(screen, (255, 0, 0), [x, 670, 50, 20], 0)

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
    def __init__(self, name, y):
        self._name = name
        self._y = y
    def y(self):
        return self._y

def create_bullets(bullets):
    i = 0
    for i in range(1, 6):
        new_bullet = Bullet(name = "bullet_" + str(i), y = 610)
        bullets.append(new_bullet)

def reload(bullets):
    pass

def draw_bullet(x, bullet_y):
    dew_hitbox.topleft = (x, bullet_y)

def update_bullet(x, bullet_y):
    dew_hitbox.topleft = (x, bullet_y)
    if bullet_y > -50:
        bullet_y -= 5
    return bullet_y

gameFlag = True
create_bullets(bullets)

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
        draw_bullet(x, bullet_y)
        bulletOnScreen = True
    if pressed[pygame.K_r]:
        reload(bullets)

    draw_player()
    if bulletOnScreen:
        bullet_y = update_bullet(x, bullet_y)

    screen.blit(dew, dew_hitbox)

    pygame.display.update()
    clock.tick(60)

pygame.quit()
quit()