#!/usr/bin/env python3
#  ^^^ This line doesn't matter on Windows but it makes us happy on Linux.
import pygame

screen = pygame.display.set_mode((1024,768))

input("Press enter to paint buffer 2 blue.")
screen.fill((30,60,200))
input("Press enter to flip buffers.")
pygame.display.flip()
input("Press enter to paint buffer 1 red.")
screen.fill((200,60,30))
input("Press enter to flip buffers again.")
pygame.display.flip()
input("Press enter to exit.")
pygame.quit() # Shuts down the window
