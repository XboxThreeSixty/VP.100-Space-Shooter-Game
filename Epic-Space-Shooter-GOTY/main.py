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
bullets = []
firedBullets = []
b = -1
magIndex = 5

# Original rect
mtndew = pygame.image.load("mountaindew.png").convert_alpha()
dew = pygame.transform.scale(mtndew, (50, 50))
dew_hitbox = dew.get_rect()

# Functions
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
    i = 0
    if len(bullets) < 1:
        firedBullets.clear()
        for i in range(1, 6):
            new_bullet = Bullet(name = "bullet_" + str(i), x = 1, y = 610, image = dew.copy())
            bullets.append(new_bullet)
        print("Magazine: 5/5 bullets")

def draw_bullet(x, bullets, b, magIndex):
    if magIndex >= 0:
        bullets[b]._rect.x = x
        bullets[b].topleft = (bullets[b].get_x(), bullets[b].get_y())
        print("Magazine: "+str(magIndex)+"/5 bullets")

        if len(bullets) > 0 and bullets[b].get_y() <= -50:
            bullets[b].y(610)

def update_bullet(i):
    bullets[i]._rect.y = bullets[i].get_y()
    if bullets[i].get_y() > -50:
        bullets[i].y(bullets[i].get_y() - 15)

runningGame = True
create_bullets(bullets)

pygame.key.set_repeat(400, 400)

# Game Loop
while runningGame:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            runningGame = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                if b < 4:
                    b += 1
                elif b == 4:
                    b = 0
                
                magIndex -= 1
                draw_bullet(x, bullets, b, magIndex)
            if event.key == pygame.K_r:
                if magIndex != 5:
                    magIndex = 5
                    print("Magazine: 5/5 bullets")

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

    # if len(bullets) > 0:
    for i in range(len(bullets)):
        screen.blit(bullets[i]._image, bullets[i]._rect)

    pygame.display.update()
    clock.tick(60)

pygame.quit()
quit()