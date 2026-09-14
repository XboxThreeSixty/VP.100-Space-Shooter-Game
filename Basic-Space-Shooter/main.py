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
pygame.display.update()
clock.tick(60)

gameFlag = True

while gameFlag:
    # game stuff
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            gameFlag = False

pygame.quit()
quit()