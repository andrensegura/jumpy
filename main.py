import pygame,sys
from pygame.locals import *

pygame.init()
fpsClock = pygame.time.Clock()

# window surface object
windowSurface = pygame.display.set_mode((400,300))
pygame.display.set_caption("Jumpy")

# colors
red    = pygame.Color(255,123,123)
blue   = pygame.Color(125,148,224)
yellow = pygame.Color(255,219,127)
backgr = pygame.Color(110,110,110)
black  = pygame.Color(0,0,0)
white  = pygame.Color(255, 255, 255)

# game loop
while True:
    windowSurface.fill(backgr)

    for event in pygame.event.get():
        if (event.type == QUIT) or (event.type == KEYDOWN and event.key == K_ESCAPE):
            pygame.quit()
            sys.exit()
    
    pygame.display.update()
    fpsClock.tick(30)