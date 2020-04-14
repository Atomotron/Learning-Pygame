#!/usr/bin/env python3
import pygame,math
from pygame.locals import *

screen = pygame.display.set_mode((1024,768))

# Load the image, and "convert" it (optional step) into an optimal format.
image = pygame.image.load("../img/spriteanim.png").convert_alpha()
maximum_shrug = image.subsurface(pygame.Rect((364,0),(90,145)))

# Make a rotated version of the image
rotated_image = pygame.transform.rotozoom(maximum_shrug,45,2)

clock = pygame.time.Clock() # A clock to keep track of time
frame = 0
pos = (0,0) # position for animation
while True:
    frame += 1
    clock.tick(60) # If we go faster than 60fps, stop and wait.
    for event in pygame.event.get(): # Get everything that's happening
        if event.type == QUIT: # If someone presses the X button
            pygame.quit() # Shuts down the window
            exit()
        elif event.type == KEYDOWN and event.key == K_ESCAPE:
            pygame.quit()
            exit()
    #Draw a black square to erase if the right button is pressed
    if pygame.mouse.get_pressed()[2]:
        pygame.draw.rect(
            screen,
            (0,0,0), #black
            pygame.Rect(
                pygame.mouse.get_pos(),
                maximum_shrug.get_size(), # width and height
            )
        )
    #Draw the image where the mouse is, if the left button is pressed
    if pygame.mouse.get_pressed()[0]:
        screen.blit(maximum_shrug,pygame.mouse.get_pos())

    # Draw a little animation
    pygame.draw.rect( # Black rectangle at previous position
        screen,
        (0,0,0), #black
        pygame.Rect(
            pos,maximum_shrug.get_size(), # width and height
        )
    )
    pos = (int(math.sin(frame/120)*300)+screen.get_width()//2,0)
    screen.blit(maximum_shrug,pos) # Image at new position
    
    pygame.display.flip()
