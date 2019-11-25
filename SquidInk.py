import random
import os, sys
import pygame
import Load
from pygame.locals import *
import Game

class SquidInk(pygame.sprite.Sprite):
    """sprite for apply_squiddy when squid ink is displayed"""

    def __init__(self, game, rounds, startPos = (250,250)):
        pygame.sprite.Sprite.__init__(self)
        self.game = game
        self.image, self.rect = Load.load_image("ink.png", None, (468,468))
        self.initial_round = self.game.turns
        self.rounds = rounds
        game.allsprites.add(self)
        screen = pygame.display.get_surface()
        self.startPos = startPos
        self.rect.center = self.game.translatePoint(startPos)
        self.onScreen = True

    def update(self):
        self.rect.center = self.game.translatePoint(self.startPos)
        if self.game.turns == self.initial_round + self.rounds:
            self.kill()
