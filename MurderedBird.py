import pygame
from Load import *
import Game

GRAVITY = 9
class MurderedBird(pygame.sprite.Sprite):
    move = 9
    bird_size = (50,50)

    def __init__(self, game, startPos = (100,100)):

        pygame.sprite.Sprite.__init__(self)
        self.groups = [game.allsprites,game.murdered]
        self.image, self.rect = load_image('scooter.png', -1, startPos)
        screen = pygame.display.get_surface()
        self.dropping = False
        self.stationary = False
        self.game = game
        self.rect.center = self.game.translatePoint(startPos)
        self.area = screen.get_rect()
        for each in self.groups:
            each.add(self)

    def update(self):
        if not self.stationary:
            if self.dropping:
                self.drop()
            else:
                self.fly()

    def fly(self):
        """move the bird across the screen, and turn at the ends"""
        newpos = self.rect.move((self.move, 0))
        area = self.game.calcScreenRect()
        if not area.contains(newpos):
            if self.rect.left < self.area.left or \
                    self.rect.right > self.area.right:
                self.move = -self.move
                newpos = self.rect.move((self.move, 0))
                self.image = pygame.transform.flip(self.image, 1, 0)
        self.rect = newpos

    def drop(self):
        """make the bird fall"""
        newpos = self.rect.move((0, GRAVITY))
        self.rect = newpos
        if self.rect.top >= self.area.height:
            print("DEAD!")
            self.kill()
