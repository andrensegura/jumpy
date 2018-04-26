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

# determines collision direction
def collision_direction(subj, obj):
    bottom = abs(subj.bottom - obj.top)
    top    = abs(subj.top - obj.bottom)
    left   = abs(subj.left - obj.right)
    right  = abs(subj.right - obj.left)

    direction = min([bottom, top, left, right])

    if direction == bottom: return "bottom"
    if direction == top: return "top"
    if direction == left: return "left"
    if direction == right: return "right"
    

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
        self.xvel = 0

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
        if self.xvel != 0:
            self.rect.x += self.xvel

class Block(Entity):
    def __init__(self, x, y):
        Entity.__init__(self, black, x, y)

class Creature(Entity):
    def __init__(self, color, x, y, walls):
        Entity.__init__(self, color, x, y, gravity=True)
        self.walls = walls

    def collide(self):
        collisions = pygame.sprite.spritecollide(self, self.walls, False)
        # UNCOMMENT THE FOLLOWING TWO LINES TO ALLOW CREATURES TO FALL
        #if not collisions:
        #    self.grounded = False
        for block in collisions:
            direction = collision_direction(self.rect, block.rect)
            if direction == 'bottom':
                self.rect.bottom = block.rect.top
                self.grounded = True
            elif direction == 'top':
                self.rect.top = block.rect.bottom
            elif direction == 'left':
                self.rect.left = block.rect.right
                self.xvel = 0
            elif direction == 'right':
                self.rect.right = block.rect.left
                self.xvel = 0

    def update(self):
        self.collide()
        Entity.update(self)

class Player(Creature):
    def __init__(self, x, y, walls):
        Creature.__init__(self, red, x, y, walls)
        self.max_xvel = 5
        # -1: left, 0: neither, 1: right
        self.direction = 0

    def update(self):
        self.xvel += self.direction / 5
        if abs(self.xvel) > self.max_xvel:
            self.xvel = self.max_xvel * self.direction
        # slow down
        if (abs(self.xvel) != 0) and self.grounded:
            self.xvel -= 0.1 * (self.xvel / abs(self.xvel))
            self.xvel = round(self.xvel, 1)
        Creature.update(self)
        print(self.xvel)

    def jump(self):
        self.grounded = False
        self.yvel = -5

# controller class
class Controller():
    def __init__(self, player):
        self.player = player
        self.jump  = [K_SPACE, K_w, K_UP]
        self.left  = [K_a, K_LEFT]
        self.right = [K_d, K_RIGHT]

    def update(self):
        for event in pygame.event.get():
            if (event.type == QUIT) or (event.type == KEYDOWN and event.key == K_ESCAPE):
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONUP:
                global run
                run = True
            elif event.type == KEYDOWN:
                if event.key in self.jump:
                    player.jump()
                elif event.key in self.left:
                    player.direction = -1
                elif event.key in self.right:
                    player.direction = 1
            elif event.type == KEYUP:
                if event.key in (self.left + self.right):
                    player.direction = 0

# game loop
blocks = pygame.sprite.Group()
for i in range(0,12):
    blocks.add(Block(100 + i*25, 275))
    blocks.add(Block(100 + i*25, 20))
blocks.add(Block(275, 250))
blocks.add(Block(275, 225))
blocks.add(Block(275, 200))

player = Player(125, 75, blocks)
creatures = pygame.sprite.Group()
creatures.add(Entity(blue, 125, 100))
creatures.add(player)
creatures.add(Creature(yellow, 225, 65, blocks))

controller = Controller(player)

# for testing. when you click the game, it will start. will eventually be a start menu.
run = False

while True:
    windowSurface.fill(backgr)

    controller.update()
    
    # update creatures and check for collision
    if run:
        for entity in creatures:
            entity.update()

    
    blocks.draw(windowSurface)
    creatures.draw(windowSurface)
    pygame.display.update()
    fpsClock.tick(60)