#!/usr/bin/env python3
import pygame,math
from pygame.locals import *

screen = pygame.display.set_mode((500,768))

# Load the image, and "convert" it (optional step) into an optimal format.
image = pygame.image.load("../img/spriteanim.png").convert_alpha()

# "Blitting" means copying image data as quickly as possible
# screen.blit(...) copies image data to the screen
screen.blit(
    image, # The source of the image data to draw
    (0,0)  # The coordinates to draw it at
) 

# Take the area starting at (364,0), 90 pixels wide and 145 pixels tall
maximum_shrug = image.subsurface(
    pygame.Rect(
        (364,0), # Top left corner (x,y)
        (90,145) # (width,height)
    ) # The rectangle to clip out
)
# ...and draw it at (100,100)
screen.blit(maximum_shrug,(100,200))

# Make a rotated version of the image
rotated_image = pygame.transform.rotozoom(
    maximum_shrug, # source image to transform
    45, # angle in degrees
    2 # scaling factor (2 -> twice as big)
)
screen.blit(rotated_image,(100,400))

# Flip the buffers
pygame.display.flip()

# We want to make the exit button work...
# So it's time to have something called an "event loop."
while True:
    events = pygame.event.get() # A list of everything that happened since we last checked
    for event in events: # Get everything that's happening
        if event.type == QUIT: # If someone presses the X button
            pygame.quit() # Shuts down the window
            exit()
        elif event.type == KEYDOWN and event.key == K_ESCAPE:
            pygame.quit()
            exit()
