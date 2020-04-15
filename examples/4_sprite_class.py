#!/usr/bin/env python3
import random,math
import pygame
from pygame import Rect
from pygame.locals import *

pygame.init()
screen = pygame.display.set_mode((1024,768))

# Load image assets
player_sheet = pygame.image.load("../img/spritecolor_v2.png").convert_alpha()
spritesheet = pygame.image.load("../img/sprites.png").convert_alpha()
background = pygame.image.load("../img/PyBgrd2_Dunes.png").convert_alpha()

source_rects = {
    'man'   : Rect((0,0),(48*2,48*3)),
    'turret': Rect((48*2,0),(48*2,48*3)),
    'dragon': Rect((48*4,0),(48*2,48*3)),
    'sword' : Rect((48*6,0),(48*2,48*3)),
    'axe'   : Rect((48*8,0),(48*2,48*3)),
    'hammer': Rect((48*10,0),(48*2,48*3)),
    'werewolf':Rect((48*12,0),(48*4,48*3)),
    'warrior':Rect((48*16,0),(48*2,48*3)),
    'royal' : Rect((48*18,0),(48*2,48*3)),
    'apple' : Rect((0,48*3),(48*2,48*2)),
    'cherry': Rect((48*2,48*3),(48*2,48*2)),
    'poultry':Rect((48*4,48*3),(48*2,48*2)),
    'meat'  : Rect((48*6,48*3),(48*2,48*2)),
    'lake'  : Rect((48*8,48*3),(48*8,48*2)),
    'angel' : Rect((48*16,48*3),(48*2,48*3)),
    'devil' : Rect((48*18,48*3),(48*2,48*3)),
    'flame' : Rect((0,48*5),(48*4,48*2)),
    'jet'   : Rect((48*4,48*5),(48*5,48*2)),
    'fire'  : Rect((48*9,48*5),(48*2,48*3)),
    'fir'   : Rect((48*11,48*5),(48*2,48*3)),
    'oak'   : Rect((48*13,48*5),(48*2,48*3)),
    'flower': Rect((48*15,48*6),(48,48*2)),
    'shrub' : Rect((48*16,48*6),(48*2,48*2)),
    'block' : Rect((48*18,48*6),(48*2,48*2)),
    'tallgrass1': Rect((0,48*9),(48,48*2)),
    'tallgrass2': Rect((48,48*9),(48*2,48*2)),
    'castle': Rect((48*3,48*8),(48*8,48*4)),
    'rock'  :Rect((48*12,48*9),(48*3,48*2)),
    'boulder':Rect((48*15,48*8),(48*3,48*3)),
    'outcrop':Rect((48*18,48*8),(48*2,48*3)),
    'widegrass'  :Rect((48*13,48*11),(48*5,48*1)),
    'grass'  :Rect((48*18,48*11),(48*2,48*1)),
}

class World(object):
    def __init__(self,background,screen_rect):
        # Foreground drawing
        self.things = []
        # Background drawing
        self.dirty_rects = [screen_rect] # We must draw the whole background on startup
        self.background = background
    def draw(self,screen):
        for rect in self.dirty_rects:
            screen.blit(self.background,(0,0),rect)
        for thing in self.things:
            thing.draw(screen)

class Sprite(object):
    def __init__(self,world,spritesheet,source_rect,pos,theta=0):
        self.dirty = True # True if this sprite has changed and must be updated
        self.sprite_dirty = True # True if the cached sprite does not match what the sprite should be
        self.world = world
        self.spritesheet = spritesheet
        self.source_rect = source_rect
        self.rect = None # To be set by position setter
        self.theta = theta
        self.pos = pos
        world.things.append(self)
    def flag_dirty(self):
        if not self.dirty:
            self.world.dirty_rects.append(self.rect)
        self.dirty = True
    
    @property
    def sprite(self):
        if self.sprite_dirty:
            self._sprite = pygame.transform.rotozoom(
                spritesheet.subsurface(self.source_rect),
                self.theta,
                1,
            )
            self.sprite_dirty = False
        return self._sprite        
    @property
    def theta(self):
        return self._theta
    @theta.setter
    def theta(self,t):
        self.flag_dirty()
        self.sprite_dirty = True
        self._theta = t
    @property
    def source_rect(self):
        return self._source_rect
    @source_rect.setter
    def source_rect(self,r):
        self.flag_dirty()
        self.sprite_dirty = True
        self._source_rect = r
    @property
    def pos(self):
        return self._pos
    @pos.setter
    def pos(self,x):
        self.flag_dirty()
        self._pos = x
        self.rect = self.sprite.get_rect().move(int(x[0]),int(x[1]))
    def draw(self,screen):
        screen.blit(self.sprite,self.rect.topleft)

if __name__ == "__main__":
    clock = pygame.time.Clock() # A clock to keep track of time
    world = World(background,screen.get_rect())
    thing = Sprite(
            world,
            spritesheet,
            source_rects['man'],
            (0,0),
    )
    while True:
        clock.tick(60) # If we go faster than 60fps, stop and wait.
        for event in pygame.event.get(): # Get everything that's happening
            if event.type == QUIT: # If someone presses the X button
                pygame.quit() # Shuts down the window
                exit()
            elif event.type == KEYDOWN and event.key == K_ESCAPE:
                pygame.quit()
                exit()
        if random.randrange(60) == 0:
            thing.theta = random.uniform(0,360)
        if random.randrange(60) == 0:
            thing.source_rect = source_rects[random.choice(list(source_rects))]
        if random.randrange(60) == 0:
            thing.pos = (random.randrange(900),random.randrange(700))
        world.draw(screen)
        pygame.display.flip()
