import pygame
import os
os.environ['SDL_VIDEO_WINDOW_POS'] = "%d,%d" % (0,0)

pygame.init()

screenWidth = 800
screenHeight = 600

screen = pygame.display.set_mode((screenWidth, screenHeight))
pygame.display.set_caption("Basic Space Shooter")
screen.fill((0, 0, 0))
clock = pygame.time.Clock()

x = 75
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
        if x < 750:
            x += 3
        else: 
            x += 0

gameFlag = True

while gameFlag:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            gameFlag = False

    pressed = pygame.key.get_pressed()
    if pressed[pygame.K_a]:
        move_player("left")
    if pressed[pygame.K_d]:
        move_player("right")

    draw_player()

    pygame.display.update()
    clock.tick(60)

pygame.quit()
quit()