import pygame
from Load import *
import Game

numb_killed = 0
GRAVITY = 1
class MurderedBird(pygame.sprite.Sprite):
    move = 3
    bird_size = (50,50)
    image_dict = {"BIRDIE": "new_dead_birdie.png",
                    "FATSO": "new_dead_fatso.png",
                    "SQUIDDY": "new_dead_squidbird.png",
                    "INVINCIBLE": "new_dead_invincible.png",
                    "TREE": "new_dead_tree.png"}


    def __init__(self, game, startPos, type):
        #need add type
        pygame.sprite.Sprite.__init__(self)
        self.groups = [game.allsprites,game.murdered]
        self.image, self.rect = load_image(self.image_dict[type], -1, self.bird_size)
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
