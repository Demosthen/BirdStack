import os, sys
import pygame
from pygame.locals import *
from Game import Game

#if not pygame.font: print('Warning, fonts disabled')
#if not pygame.mixer: print('Warning, sound disabled')
game = Game()
msg = None
while msg != "END":
    msg = game.run()
    print("hdkfkfufkf")
    if msg == "RESTART":
        game = Game()
