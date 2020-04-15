#!/usr/bin/env python3
import pygame,math
from pygame.locals import *

pygame.init()
screen = pygame.display.set_mode((1024,768))

# Load the image, and "convert" it (optional step) into an optimal format.
image = pygame.image.load("../img/spriteanim.png").convert_alpha()
background = pygame.image.load("../img/PyBgrd2_Dunes.png").convert_alpha()

unclick = pygame.mixer.Sound("../sounds/select.ogg")
click = pygame.mixer.Sound("../sounds/deselect.ogg")

def erase(rect): # Draw the background over an area to "erase" what's there.
    screen.blit(background,rect.topleft,rect)
erase(
    screen.get_rect() # A rectangle that covers the whole screen.
)

# Looping shrug
shrug_levels = [
    image.subsurface(pygame.Rect((364-90*4,0),(90,145))),
    image.subsurface(pygame.Rect((364-90*3,0),(90,145))),
    image.subsurface(pygame.Rect((364-90*2,0),(90,145))),
    image.subsurface(pygame.Rect((364-90,0),(90,145))),
    image.subsurface(pygame.Rect((364,0),(90,145))),
    image.subsurface(pygame.Rect((364-90,0),(90,145))),
    image.subsurface(pygame.Rect((364-90*2,0),(90,145))),
    image.subsurface(pygame.Rect((364-90*3,0),(90,145))),
]
shrug_level = 0

clock = pygame.time.Clock() # A clock to keep track of time
frame = 0 # Frame counter
pos = (0,0) # position for animation
while True:
    frame += 1

    # Advance the shrug level, wrapping it around once it reaches the end
    if frame % 6 == 0:
        shrug_level = (shrug_level + 1) % len(shrug_levels)
    
    clock.tick(60) # If we go faster than 60fps, stop and wait.
    for event in pygame.event.get(): # Get everything that's happening
        if event.type == QUIT: # If someone presses the X button
            pygame.quit() # Shuts down the window
            exit()
        elif event.type == KEYDOWN and event.key == K_ESCAPE:
            pygame.quit()
            exit()
        elif event.type == pygame.MOUSEBUTTONDOWN:
            click.play()
        elif event.type == pygame.MOUSEBUTTONUP:
            unclick.play()
    #Draw a black square to erase if the right button is pressed
    pressed_mouse_buttons = pygame.mouse.get_pressed() # a list of mouse buttons
    if pressed_mouse_buttons[2]: # 2nd element: right button
        erase(
            pygame.Rect( # The rectangle to draw
                pygame.mouse.get_pos(), # position
                shrug_levels[shrug_level].get_size(), # width and height
            )
        )
    #Draw the image where the mouse is, if the left button is pressed
    if pressed_mouse_buttons[0]: # 2nd element: left button
        screen.blit(shrug_levels[shrug_level],pygame.mouse.get_pos())

    ### Draw a little animation
    # Black rectangle at previous position erases old image of man
    erase(
        pygame.Rect( # The rectangle to draw
            pos,shrug_levels[shrug_level].get_size(), # width and height
        )
    )
    # Compute new position
    pos = (int(math.sin(frame/120)*300)+screen.get_width()//2,0)
    # Draw new image of man at new position
    screen.blit(shrug_levels[shrug_level],pos) 

    # Remember, once you're done drawing and want people to see what you drew,
    # you have to flip the buffer.
    pygame.display.flip()
