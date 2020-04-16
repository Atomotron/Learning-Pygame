#!/usr/bin/env python3
import pygame,math
from pygame.locals import *

pygame.init()

screenHeight = 768
screenWidth = 1024

screen = pygame.display.set_mode((screenWidth,screenHeight))


image = pygame.image.load("../img/spriteanim_v2.png").convert_alpha()
gameSprite = pygame.image.load("../img/spritecolor_v2.png").convert_alpha()

background = pygame.image.load("../img/testBackground.png").convert_alpha()

unclick = pygame.mixer.Sound("../sounds/select.ogg")
click = pygame.mixer.Sound("../sounds/deselect.ogg")


class Devil():
    def __init__(self,sprite,pos):
        self.sprite = sprite
        self.pos = pos
        
    def draw(self,screen):
        screen.blit(self.sprite,self.pos)
        
    def move(self,x,y,direction = 0):
        erase(pygame.Rect(devil.pos,devil.sprite.get_size()))
        
   #     if direction !=0:
    #        if direction == 1 :
     #           self.sprite = pygame.transform.flip(self.sprite,1,0)
      #      else:
        #        self.sprite = pygame.transform.flip(self.sprite,0,1)
        self.pos[0] = x
        self.pos[1] = y
        devil.draw(screen)
        
        

castleRect = gameSprite.subsurface(pygame.Rect((48*3,48*8),(48*8,48*4)))
fireplaceSprite = gameSprite.subsurface(pygame.Rect((430,240),(100,150)))
guyStillSprite = image.subsurface(pygame.Rect((364,0),(90,145)))
treeSprite = gameSprite.subsurface(pygame.Rect((48*13,48*5),(48*2,48*3)))
shrubSprite = gameSprite.subsurface(pygame.Rect((48*16,48*6),(48*2,48*2)))
cometSprite = gameSprite.subsurface(pygame.Rect((48*4,48*5),(48*5,48*2)))

angle =0

fireplaceImage2 = pygame.transform.rotozoom(fireplaceSprite,0,1.4)
guy = pygame.transform.rotozoom(guyStillSprite,0,1.8)
castle = pygame.transform.rotozoom(castleRect,3,1.6)
tree = pygame.transform.rotozoom(treeSprite,0,2)
shrub = pygame.transform.rotozoom(shrubSprite,0,1.4)
comet = pygame.transform.rotozoom(cometSprite,angle,0.65)


def erase(rect):
    screen.blit(background,rect.topleft,rect)
    screen.blit(castle,((screenWidth/2)-600,230))
    screen.blit(shrub,((screenWidth/2)-400,450))
    screen.blit(tree,((screenWidth/2)+220,250))
    screen.blit(fireplaceImage2,((screenWidth/2)+80,440))
    screen.blit(guy,((screenWidth/2)+175,430))


    #if random.randrange(0,2,1) :
     #   randX1= random.randrange(100,(screenWidth/2)-100)
      #  randY1= random.randrange((screenHeight/2)+100,screenHeight)
       # randX2= random.randrange((screenWidth/2)+200,screenWidth-80)
        #randY2= random.randrange((screenHeight/2),screenHeight-382)
       # screen.blit(shrub,(randX1,randY1))
        #screen.blit(tree,(randX2,randY2))
        #done =1
    #else:
     #   randX1= random.randrange(100,(screenWidth/2)-100)
      #  randY1= random.randrange((screenHeight/2)+100,screenHeight)
       # randX2= random.randrange((screenWidth/2)+200,screenWidth-80)
        #randY2= random.randrange((screenHeight/2),screenHeight-382)
        #screen.blit(shrub,(randX2,randY2))
        #screen.blit(tree,(randX1,randY1))
        #done = 1
  
erase(screen.get_rect())



clock = pygame.time.Clock() 
frame = 0
count = 0

devil = Devil(gameSprite.subsurface(pygame.Rect((48*18,48*3),(48*2,48*3))),[50,50])


while True:
    frame += 1

    clock.tick(60) 
    for event in pygame.event.get(): 
        if event.type == QUIT: 
            pygame.quit() 
            exit()
        elif event.type == KEYDOWN and event.key == K_ESCAPE:
            pygame.quit()
            exit()
    
    erase(pygame.Rect((1200-count,220-(count**0.7)),comet.get_size()))
    devil.draw(screen)
    
    pressed = pygame.key.get_pressed()
    if pressed[pygame.K_w]: 
        devil.move(devil.pos[0],devil.pos[1]-10)
    if pressed[pygame.K_s]:
        devil.move(devil.pos[0],devil.pos[1]+10)
    if pressed[pygame.K_d]:
        devil.move(devil.pos[0]+10,devil.pos[1],1)
    if pressed[pygame.K_a]:
        devil.move(devil.pos[0]-10,devil.pos[1],-1)
    
    

    pos = (1050-count, 200-(count**0.7))
    screen.blit(comet,pos)
    
    if count > 1450 :
        count = 0
        
    count+=1.8

    pygame.display.flip()
