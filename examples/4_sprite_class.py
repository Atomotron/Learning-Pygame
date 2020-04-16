#!/usr/bin/env python3
import random,math
import numpy as np
import pygame
from pygame import Rect
from pygame.locals import *

pygame.init()
screen = pygame.display.set_mode((1024,768))

# Configuration
PLAYER_SPEED = 1
WEREWOLF_SPEED = 0.2
GRAVITY = np.array((0.0,0.01))
SWORD_VELOCITY = 3
BACKGROUND_SPRITES = [
    'fir','oak','flower','shrub','tallgrass1','tallgrass2','rock','boulder','outcrop','widegrass','grass',
] # sprite names which are considered background objects

# Load image and sound assets
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

player_frames = [
    Rect((0,0),(48*2,48*3)),
    Rect((48*2,0),(48*2,48*3)),
    Rect((48*4,0),(48*2,48*3)),
    Rect((48*6,0),(48*2,48*3)),
    Rect((48*10,0),(48*2,48*3)),
]

class World(object):
    """The world contains all of the sprites, and keeps track of what rectangles
       need to be painted over by the background to erase old stuff."""
    def __init__(self,background,camera=(0,0)):
        self.player = None # A blessed, special entity.
        self.things = []
        self.actors = []
        self.reactors = []
        self.background = background
        self.camera = np.array(camera,dtype=np.float_)
    def tick(self,dt):
        for thing in self.things:
            thing.tick(dt)
        for actor in self.actors:
            for reactor in self.reactors:
                if actor.rect.colliderect(reactor.rect):
                    actor.collide(reactor)
        if self.player:
            delta = ((self.player.pos[0] - self.camera[0]) / self.background.get_rect().width) - 0.5
            speed = math.pow(delta,3)*10
            self.camera[0] += dt*speed # Rectangle integration method
    def draw(self,screen):
        # The position on the screen of the background repetition seam
        background_rect = self.background.get_rect()
        seam = (-int(self.camera[0])) % background_rect.width
        screen.blit(self.background,(seam,0),Rect((0,0),(background_rect.width - seam,background_rect.height)))
        screen.blit(self.background,(0,0),Rect((background_rect.width - seam,0),(seam,background_rect.height)))
        for thing in self.things:
            thing.draw(screen,self.camera)
    def populate(self):
        """Introduce a bunch of objects."""
        self.things = []
        self.actors = []
        self.reactors = []
        self.camera = np.array((0,0),dtype=np.float_)
        for i in range(0,100):
            Sprite(
                self,
                spritesheet,
                source_rects[random.choice(BACKGROUND_SPRITES)],
                (random.uniform(0,10000),random.uniform(550,730)),
            )
        Player(world,(100,650))
        Werewolf(world,(1000,650))
        world.z_sort()
    def z_sort(self):
        """Order drawable things by their position. Run this after introducing new objects."""
        self.things.sort(key=lambda x: x.rect.bottom)

class Sprite(object):
    """A drawable thing that sits in the world."""
    NORMAL = 0
    HURT = 0b1
    DISAPPEAR = 0b10
    WIGGLE = 0b100
    def __init__(self,world,_spritesheet,source_rect,pos,theta=0,scale=1,anim_state=0):
        self.sprite_dirty = True # True if the cached sprite does not match what the sprite should be
        self.world = world
        self.spritesheet = _spritesheet
        self.source_rect = source_rect
        self._mirrored = False
        self.theta = theta
        self.scale = scale
        self.anim_state = anim_state
        self.anim_time = 0
        self.pos = pos
        world.things.append(self)
    def clean_sprite(self):
        try:
            subsurf = self.spritesheet.subsurface(self.source_rect)
        except ValueError as e:
            raise Exception(str(self.spritesheet) + 'rect error' +str(self.source_rect)) from e
        self._sprite = pygame.transform.rotozoom(
            pygame.transform.flip(subsurf,self._mirrored,False),
            self._theta,
            self._scale,
        )
        self.sprite_dirty = False
        self.clean_rect()
    def clean_rect(self):
        if self.sprite_dirty:
            self.clean_sprite()
        sprite_rect = self._sprite.get_rect()
        self._rect = Rect(
            int(self._pos[0]-sprite_rect.width/2),
            int(self._pos[1]-sprite_rect.height/2),
            sprite_rect.width,
            sprite_rect.height,
        )
    @property
    def rect(self):
        if self.sprite_dirty:
            self.clean_sprite()
        return self._rect
    @property
    def sprite(self):
        if self.sprite_dirty:
            self.clean_sprite()
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
        self._pos = np.array(x,dtype=np.float_)
        self.clean_rect()
    @property
    def mirrored(self):
        return self._mirrored
    @mirrored.setter
    def mirrored(self,m):
        if self._mirrored != m:
            self.sprite_dirty = True
            self._mirrored = m

    def draw(self,screen,camera):
        # We draw the sprite whether we're flagged as dirty or not,
        # because we don't know whether or not another drawing operation
        # messed up our image on the screen by painting over it.
        world_pos = self.rect.topleft
        screen.blit(self.sprite,(world_pos[0]-int(camera[0]),world_pos[1]-int(camera[1])))
        sprite_rect = self.sprite.get_rect()
    def tick(self,dt): # Advance in time
        if self.anim_state & Sprite.HURT:
            half_height = self.spritesheet.get_rect().height//2
            if self.anim_time % 10 < 3 and self.source_rect.top < half_height:
                self.source_rect = self.source_rect.move(0,half_height)
            elif self.anim_time % 10 >= 3 and self.source_rect.top >= half_height:
                self.source_rect = self.source_rect.move(0,-half_height)
        if self.anim_state & Sprite.DISAPPEAR:
            self.theta += dt/2
            self.scale = self.scale - 0.003*self.scale*dt
        if self.anim_state & Sprite.WIGGLE:
            self.theta += 0.05*math.cos(self.anim_time/120)*dt
        if self.anim_state:
            self.anim_time += dt
        else:
            self.anim_time = 0

class Player(Sprite):
    NAME = "player"
    def __init__(self,world,pos):
        self.frame = 1
        super().__init__(
            world,
            playersheet,
            player_frames[self.frame],
            pos
        )
        self.dead = False
        world.reactors.append(self)
        world.player = self
        self.sword_launcher = SwordLauncher(self)
    def tick(self,dt):
        if not self.dead:
            pressed = pygame.key.get_pressed()
            if pressed[K_RIGHT] or pressed[K_d] or pressed[K_a] or pressed[K_LEFT]:
                self.anim_state |= Sprite.WIGGLE
            else:
                self.anim_state &= ~Sprite.WIGGLE
                self.theta = self.theta - 0.01*self.theta*dt
            if pressed[K_RIGHT] or pressed[K_d]:
                self.pos[0] += dt*PLAYER_SPEED
                self.mirrored = True
            if pressed[K_LEFT] or pressed[K_a]:
                self.pos[0] -= dt*PLAYER_SPEED
                self.mirrored = False
        super().tick(dt)
    def die(self):
        self.dead = True
        self.anim_state |= Sprite.DISAPPEAR | Sprite.HURT
    def throw_sword_at(self,screen_pos):
        screen_pos = np.array(screen_pos,dtype=np.float_)
        target_pos = self.world.camera + screen_pos
        
        Sword(self.world,target_pos,(0,-2.5))

class Werewolf(Sprite):
    NAME = "werewolf"
    def __init__(self,world,pos):
        super().__init__(
            world,
            spritesheet,
            source_rects['werewolf'],
            pos
        )
        self.dead = False
        self.interacting = True
        self.anim_state |= Sprite.WIGGLE # always walking
        world.actors.append(self)
        world.reactors.append(self)
    def tick(self,dt):
        if not self.dead:
            self.pos[0] -= dt * WEREWOLF_SPEED
        elif self.scale < 0.01:
            world.things.remove(self)
        super().tick(dt)
    def die(self):
        self.dead = True
        self.anim_state |= Sprite.DISAPPEAR | Sprite.HURT
        world.actors.remove(self)
        world.reactors.remove(self)
    def collide(self,reactor):
        if reactor.NAME == "player":
            reactor.die()

class Sword(Sprite):
    def __init__(self,world,pos,vel,theta):
        super().__init__(
            world,
            spritesheet,
            source_rects['sword'],
            pos,
            theta=theta
        )
        self.vel = np.array(vel,dtype=np.float_)
        world.actors.append(self)
    def tick(self,dt):
        self.theta += dt*0.5
        self.pos += dt*self.vel
        self.vel += dt*GRAVITY
        super().tick(dt)
        if self.pos[1] > 800:
            world.things.remove(self)
            world.actors.remove(self)
    def collide(self,reactor):
        if reactor.NAME == "werewolf":
            reactor.die()

class SwordLauncher(Sprite):
    def __init__(self,player):
        super().__init__(
            player.world,
            spritesheet,
            source_rects['sword'].move(0,600),
            player.pos
        )
        self.player = player
        self.launch_angle = 0
    def tick(self,dt):
        target_pos = self.world.camera + np.array(pygame.mouse.get_pos())
        target_vector = target_pos - self.player.pos
        self.launch_angle = min(-math.pi/4,max(-3*math.pi/4,math.atan2(target_vector[1],target_vector[0])))
        dx = np.array((math.cos(self.launch_angle),math.sin(self.launch_angle))) * 48*3
        self.pos = self.player.pos + dx
        self.theta = -(self.launch_angle / (2*math.pi) * 360) + 130
    def launch(self):
        vel = np.array((math.cos(self.launch_angle),math.sin(self.launch_angle)))*SWORD_VELOCITY
        Sword(self.world,self.player.pos,vel,self.theta)

if __name__ == "__main__":
    clock = pygame.time.Clock() # A clock to keep track of time
    world = World(background)
    world.populate()
    keep_on_stepping = True
    while keep_on_stepping:
        dt = clock.tick(30) # If we go faster than 60fps, stop and wait.
        for event in pygame.event.get(): # Get everything that's happening
            if event.type == QUIT: # If someone presses the X button
                keep_on_stepping = False
            elif event.type == KEYDOWN and event.key == K_ESCAPE:
                keep_on_stepping = False
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                world.player.sword_launcher.launch()
        world.tick(dt)
        world.draw(screen)
        pygame.display.flip()
    pygame.quit()
