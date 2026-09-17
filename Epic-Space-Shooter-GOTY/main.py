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
bullet_x = 0
bullets = []
bulletOnScreen = False

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
    def __init__(self, name, y, image):
        self._name = name
        self._y = y
        self._image = image 
        self._rect = image.get_rect()
    def y(self, y):
        self._y = y
    def get_y(self):
        return self._y

def create_bullets(bullets):
    i = 0
    if len(bullets) < 1:
        for i in range(1, 6):
            new_bullet = Bullet(name = "bullet_" + str(i), y = 610, image = dew.copy())
            bullets.append(new_bullet)
        print("Magazine: 5/5 bullets")

def draw_bullet(x, bullets):
    if len(bullets) > 0:
        bullets[0]._rect.topleft = (x, bullets[0].get_y())
        # bullets.pop(0)
        if bullets[0].get_y() <= -50:
            bullets[0].y(610)
    print("Magazine: " +str(len(bullets))+"/5 bullets")

def update_bullet():
    bullets[0]._rect.y = bullets[0].get_y()
    if bullets[0].get_y() > -50:
        bullets[0].y(bullets[0].get_y() - 15)

gameFlag = True
create_bullets(bullets)

pygame.key.set_repeat(400, 400)

# Game Loop
while gameFlag:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            gameFlag = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                draw_bullet(x, bullets)
                bulletOnScreen = True
            if event.key == pygame.K_r:
                create_bullets(bullets)

    pressed = pygame.key.get_pressed()
    if pressed[pygame.K_a]:
        move_player("left")
    if pressed[pygame.K_d]:
        move_player("right")

    draw_player()
    if bulletOnScreen:
        update_bullet()

    screen.blit(bullets[0]._image, bullets[0]._rect)

    pygame.display.update()
    clock.tick(60)

pygame.quit()
quit()