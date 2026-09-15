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
clock.tick(60)

x = 75

gameFlag = True

while gameFlag:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            gameFlag = False

    pressed = pygame.key.get_pressed()
    if pressed[pygame.K_a]:
        screen.fill((0, 0, 0))
        if x > 0:
            x -= 3
        else:
            x -= 0
    if pressed[pygame.K_d]:
        screen.fill((0, 0, 0))
        if x < 750:
            x += 3
        else: 
            x += 0

    pygame.draw.rect(screen, (255, 0, 0), [x, 550, 50, 20], 2)

    pygame.display.update()
    clock.tick(60)

pygame.quit()
quit()