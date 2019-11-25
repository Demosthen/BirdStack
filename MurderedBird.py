import pygame
from Load import *
import Game

numb_killed = 0
GRAVITY = 1
class MurderedBird(pygame.sprite.Sprite):
    move = 3
    bird_size = (50,50)


    def __init__(self, game, startPos):

        pygame.sprite.Sprite.__init__(self)
        self.groups = [game.allsprites,game.murdered]
        self.image, self.rect = load_image('new_dead_birdie.png', -1, self.bird_size)
        screen = pygame.display.get_surface()
        self.final_drawn = False
        #keep track of how many killed, how many types killed?
        self.game = game
        self.rect.center = self.game.translatePoint(startPos)
        self.area = screen.get_rect()
        self.onScreen = True
        for each in self.groups:
            each.add(self)

    def update(self):
        self.drop()

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
        global numb_killed
        newpos = self.rect.move((0, GRAVITY))
        self.rect = newpos
        area = self.game.calcScreenRect()
        if self.rect.top >= area.bottom:
            numb_killed+=1
            print("DEAD!", numb_killed)
            self.kill()
