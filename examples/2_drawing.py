#!/usr/bin/env python3
import pygame,math
from pygame.locals import *

screen = pygame.display.set_mode((500,768),pygame.SRCALPHA)

# Load the image, and "convert" it (optional step) into an optimal format.
image = pygame.image.load("../img/spriteanim.png").convert_alpha()

screen.blit(image,(0,0)) # Put the top left of the image at 0,0

# Take the area starting at (364,0), 90 pixels wide and 145 pixels tall
maximum_shrug = image.subsurface(pygame.Rect((364,0),(90,145)))
# ...and draw it at (100,100)
screen.blit(maximum_shrug,(100,200))

# Make a rotated version of the image
rotated_image = pygame.transform.rotozoom(maximum_shrug,45,2)
screen.blit(rotated_image,(100,400))

# We want to make the exit button work...
# So it's time to have something called an "event loop."
while True:
    for event in pygame.event.get(): # Get everything that's happening
        if event.type == QUIT: # If someone presses the X button
            pygame.quit() # Shuts down the window
            exit()
        elif event.type == KEYDOWN and event.key == K_ESCAPE:
            pygame.quit()
            exit()
    # Flip the buffers
    pygame.display.flip()
