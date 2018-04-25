import pygame,sys
from pygame.locals import *

pygame.init()
fpsClock = pygame.time.Clock()

# window surface object
WIN_WIDTH  = 480
WIN_HEIGHT = 300
windowSurface = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))
pygame.display.set_caption("Jumpy")

# world constants
# basing these things off of the window means resizing can be an option.
# you can tweak these until the physics feel right
GRAVITY       = WIN_HEIGHT / 2000
TERM_VELOCITY = WIN_HEIGHT / 20
ENT_WIDTH     = WIN_HEIGHT / 10
ENT_HEIGHT    = WIN_HEIGHT / 10

# colors
red    = pygame.Color(255,123,123)
blue   = pygame.Color(125,148,224)
yellow = pygame.Color(255,219,127)
backgr = pygame.Color(110,110,110)
black  = pygame.Color(0,0,0)
white  = pygame.Color(255, 255, 255)        

#entities
class Entity(pygame.sprite.Sprite):
    def __init__(self, color, x, y, gravity=False):
        pygame.sprite.Sprite.__init__(self)

        self.image = pygame.Surface([ENT_WIDTH, ENT_WIDTH])
        self.image.fill(color)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

        self.gravity = gravity
        self.yvel = 0

        self.grounded = False

    def update(self):
        if self.gravity:
            if self.grounded:
                self.yvel = 0
            else:
                self.rect.y += self.yvel
                self.yvel += GRAVITY
                if self.yvel > TERM_VELOCITY:
                    self.yvel = TERM_VELOCITY

class Block(Entity):
    def __init__(self, x, y):
        Entity.__init__(self, black, x, y)

class Creature(Entity):
    def __init__(self, color, x, y, walls):
        Entity.__init__(self, color, x, y, gravity=True)
        self.walls = walls
    
    def collide_walls(self):
        for block in pygame.sprite.spritecollide(self, self.walls, False):
            if (block.rect.top <= self.rect.bottom) and (block.rect.bottom >= self.rect.bottom):
                self.rect.bottom = block.rect.top
                self.grounded = True
            if (block.rect.bottom >= self.rect.top) and (block.rect.top <= self.rect.top):
                self.rect.top = block.rect.bottom
                self.yvel = 0

    def update(self):
        self.collide_walls()
        Entity.update(self)

class Player(Creature):
    def __init__(self, x, y, walls):
        Creature.__init__(self, red, x, y, walls)

    def jump(self):
        self.grounded = False
        self.yvel = -5


# game loop
blocks = pygame.sprite.Group()
blocks.add(Block(125, 200))
blocks.add(Block(125, 10))
blocks.add(Block(225, 200))

player = Player(125, 75, blocks)
creatures = pygame.sprite.Group()
creatures.add(Entity(blue, 125, 100))
creatures.add(player)
creatures.add(Creature(yellow, 225, 10, blocks))


# for testing. when you click the game, it will start. will eventually be a start menu.
run = False

while True:
    windowSurface.fill(backgr)

    for event in pygame.event.get():
        if (event.type == QUIT) or (event.type == KEYDOWN and event.key == K_ESCAPE):
            pygame.quit()
            sys.exit()
        elif event.type == pygame.MOUSEBUTTONUP:
            run = True
        elif event.type == KEYDOWN and event.key == K_SPACE:
            player.jump()
    
    # update creatures and check for collision
    if run:
        for entity in creatures:
            entity.update()

    
    blocks.draw(windowSurface)
    creatures.draw(windowSurface)
    pygame.display.update()
    fpsClock.tick(60)