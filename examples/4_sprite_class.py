#!/usr/bin/env python3
import random,math
import numpy as np
import pygame
from pygame import Rect
from pygame.locals import *

pygame.init()
screen = pygame.display.set_mode((1024,768))

# Load image assets
player_sheet = pygame.image.load("../img/spritecolor_v2.png").convert_alpha()
spritesheet = pygame.image.load("../img/sprites.png").convert_alpha()
playersheet = pygame.image.load("../img/spriteanim_v2.png").convert_alpha()
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
    """The world contains all of the sprites, and keeps track of what rectangles
       need to be painted over by the background to erase old stuff."""
    def __init__(self,background,camera=(0,0)):
        self.player = None # A blessed, special entity.
        self.things = []
        self.actors = []
        self.reactors = []
        self.background = background
        self.camera = np.array(camera)
    def tick(self,dt):
        for thing in self.things:
            thing.tick(dt)
        for actor in self.actors:
            for reactor in self.reactors:
                if actor.rect.colliderect(reactor.rect):
                    actor.collide(reactor)
        if self.player:
            delta = self.player.pos[0] - self.camera[0]
            speed = np.pow(delta,5)
            self.camera[0] += dt*speed # Rectangle integration method
    def draw(self,screen):
        # The position on the screen of the background repetition seam
        background_rect = self.background.get_rect()
        seam = (-int(self.camera[0])) % background_rect.width
        screen.blit(self.background,(seam,0),Rect((0,0),(background_rect.width - seam,background_rect.height)))
        screen.blit(self.background,(0,0),Rect((background_rect.width - seam,0),(seam,background_rect.height)))
        for thing in self.things:
            thing.draw(screen,self.camera)

class Sprite(object):
    """A drawable thing that sits in the world."""
    NORMAL = 0
    HURT = 0b1
    DISAPPEAR = 0b10
    def __init__(self,world,spritesheet,source_rect,pos,theta=0,scale=1,anim_state=0):
        self.sprite_dirty = True # True if the cached sprite does not match what the sprite should be
        self.world = world
        self.spritesheet = spritesheet
        self.source_rect = source_rect
        self.rect = None # To be set by position setter
        self.theta = theta
        self.scale = scale
        self.anim_state = anim_state
        self.anim_time = 0
        self.pos = np.array(pos)
        world.things.append(self)

    @property
    def sprite(self):
        if self.sprite_dirty:
            self._sprite = pygame.transform.rotozoom(
                spritesheet.subsurface(self.source_rect),
                self._theta,
                self._scale,
            )
            self.sprite_dirty = False
        return self._sprite
    @property
    def theta(self):
        return self._theta
    @theta.setter
    def theta(self,t):
        self.sprite_dirty = True
        self._theta = t
    @property
    def scale(self):
        return self._scale
    @scale.setter
    def scale(self,s):
        self.sprite_dirty = True
        self._scale = s
    @property
    def source_rect(self):
        return self._source_rect
    @source_rect.setter
    def source_rect(self,r):
        self.sprite_dirty = True
        self._source_rect = r
    @property
    def pos(self):
        return self._pos
    @pos.setter
    def pos(self,x):
        self._pos = x
        self.rect = self.sprite.get_rect().move(int(x[0]+self.source_rect.width/2),int(x[1]+self.source_rect.height/2))

    def draw(self,screen,camera):
        # We draw the sprite whether we're flagged as dirty or not,
        # because we don't know whether or not another drawing operation
        # messed up our image on the screen by painting over it.
        world_pos = self.rect.topleft
        screen.blit(self.sprite,(world_pos[0]-int(camera[0]),world_pos[1]-int(camera[1])))
    def tick(self,dt): # Advance in time
        if self.anim_state & Sprite.HURT:
            half_height = self.spritesheet.height//2
            if self.anim_time % 10 < 3 and self.source_rect.top < half_height:
                self.source_rect = self.source_rect.move(0,half_height)
            elif self.anim_time % 10 >= 3 and self.source_rect.top >= half_height:
                self.source_rect = self.source_rect.move(0,-half_height)
        if self.anim_state & Sprite.DISAPPEAR:
            self.theta += dt/2
            self.scale = self.scale - 0.003*self.scale*dt
        if self.anim_state != 0:
            self.anim_time += dt
        else:
            self.anim_time = 0    

if __name__ == "__main__":
    clock = pygame.time.Clock() # A clock to keep track of time
    world = World(background)
    thing = Sprite(
            world,
            spritesheet,
            source_rects['man'],
            (0,0),
            0,1,
            Sprite.HURT | Sprite.DISAPPEAR
    )
    keep_on_stepping = True
    while keep_on_stepping:
        dt = clock.tick(30) # If we go faster than 60fps, stop and wait.
        for event in pygame.event.get(): # Get everything that's happening
            if event.type == QUIT: # If someone presses the X button
                keep_on_stepping = False
            elif event.type == KEYDOWN and event.key == K_ESCAPE:
                keep_on_stepping = False
        if random.randrange(60) == 0:
            thing.theta = random.uniform(0,360)
        if random.randrange(60) == 0:
            thing.source_rect = source_rects[random.choice(list(source_rects))]
            thing.scale = 1
        if random.randrange(60) == 0:
            thing.pos = (random.randrange(900)+world.camera[0],random.randrange(700))
            thing.scale = 1
        world.tick(dt)
        world.draw(screen)
        pygame.display.flip()
    pygame.quit()
