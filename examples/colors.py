import pygame
from pygame.locals import *
from collections import defaultdict
import random,math

pygame.init()

TILE_LENGTH = 32

class Sprite(object):
    def __init__(self,pos,vel):
        self.vel = vel
        self.pos = pos
        hue = random.uniform(0,2*math.pi)
        self.color = (
            128 + int(120*math.sin(hue)),
            128 + int(120*math.sin(hue+2*math.pi/3)),
            128 + int(120*math.sin(hue+4*math.pi/3)),
        )
    def draw(self,surface):
        pygame.draw.circle(surface,self.color,(int(self.pos[0]),int(self.pos[1])),8)
    def update(self,x,g):
        r = (self.pos[0]-x[0],self.pos[1]-x[1])
        mag_r = max(math.sqrt(r[0]*r[0]+r[1]*r[1]),10)
        mag_r_3 = mag_r*mag_r
        f = (r[0]/mag_r_3*g,r[1]/mag_r_3*g)
        self.vel = (self.vel[0]+f[0],self.vel[1]+f[1])
        self.pos = (self.pos[0]+self.vel[0],self.pos[1]+self.vel[1])
        
screen_rect = pygame.Rect(0,0,1024,768)
background = pygame.Surface((screen_rect.width,screen_rect.height), pygame.SRCALPHA)
background.fill((0,0,0,1))

screen = pygame.display.set_mode((screen_rect.width,screen_rect.height)) # Open a window
pygame.display.set_caption('PyRPG') # Set the window title
clock = pygame.time.Clock() # A clock to keep track of time

sprites = set()
frame = 0
while 1:
    clock.tick(60) # 60 frames per second
    frame += 1 # Count the frames
    for event in pygame.event.get():
        if event.type == QUIT:
            exit()
        elif event.type == KEYDOWN and event.key == K_ESCAPE:
            exit()
    if frame % (60*16) > 60*8:
        theta = random.uniform(0,2*math.pi)
        pos = (screen_rect.width/2 + 60*math.cos(theta),screen_rect.height/2 + 60*math.sin(theta))
    else:
        pos = (random.uniform(0,screen_rect.width),screen_rect.height-12)
    sprites.add(
        Sprite(
            pos,
            (random.uniform(-0.1,0.1),random.uniform(-0.1,0.1))
        )
    )
    if frame % 3 == 0:
        screen.blit(background,(0,0))
    outside = []
    for sprite in sprites:
        sprite.update(pygame.mouse.get_pos(),0 if pygame.mouse.get_pressed()[0] == 0 else -32)
        if not screen_rect.collidepoint((int(sprite.pos[0]),int(sprite.pos[1]))) or random.randrange(0,1000)==0:
            outside.append(sprite)
    for sprite in outside:
        sprites.remove(sprite)
    for sprite in sprites:
        sprite.draw(screen)
    pygame.display.flip()
