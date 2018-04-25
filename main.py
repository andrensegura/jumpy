import pygame,sys
from pygame.locals import *

pygame.init()
fpsClock = pygame.time.Clock()

# window surface object
WIN_WIDTH  = 480
WIN_HEIGHT = 300
windowSurface = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))
pygame.display.set_caption("Jumpy")

# colors
red    = pygame.Color(255,123,123)
blue   = pygame.Color(125,148,224)
yellow = pygame.Color(255,219,127)
backgr = pygame.Color(110,110,110)
black  = pygame.Color(0,0,0)
white  = pygame.Color(255, 255, 255)

#entities

class Entity(pygame.sprite.Sprite):
    def __init__(self, color, x, y):
        pygame.sprite.Sprite.__init__(self)

        self.image = pygame.Surface([WIN_WIDTH / 15, WIN_WIDTH / 15])
        self.image.fill(color)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

# game loop

entities = pygame.sprite.Group()
entities.add(Entity(blue, 100, 100))

while True:
    windowSurface.fill(backgr)

    for event in pygame.event.get():
        if (event.type == QUIT) or (event.type == KEYDOWN and event.key == K_ESCAPE):
            pygame.quit()
            sys.exit()
    
    entities.draw(windowSurface)
    pygame.display.update()
    fpsClock.tick(30)