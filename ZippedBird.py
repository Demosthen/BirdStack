import random
import os, sys
import pygame
import Load
from pygame.locals import *
import Game
class ZippedBird(pygame.sprite.Sprite):
    move = 9
    bird_size = (50,50)
    image_dict = {"BIRDIE": "scooter.png",
                    "FATSO": "scooter.png",
                    "SQUIDDY": "scooter.png",
                    "INVINCIBLE": "scooter.png",
                    "TREE": "scooter.png"}


    def __init__(self, game, startPos = (100,100)):
        pygame.sprite.Sprite.__init__(self)
        self.game = game
        self.image, self.rect = self.load_spliced_image('scooter.png', startPos)
        screen = pygame.display.get_surface()
        self.stationary = False
        self.rect.center = startPos
        self.area = screen.get_rect() # TODO: UPDATE THIS ACCORDING TO GAME SCREEN POSITION
        self.left_prob_dict = {"BIRDIE": 6,
                        "FATSO": 1,
                        "SQUIDDY": 1,
                        "INVINCIBLE": 1,
                        "TREE": 1}
        self.right_prob_dict = {"BIRDIE": 6,
                        "FATSO": 1,
                        "SQUIDDY": 1,
                        "INVINCIBLE": 1,
                        "TREE": 1}
        self.effect_dict = { "FATSO": self.apply_fatso,
                        "SQUIDDY": self.apply_squiddy,
                        "INVINCIBLE": self.apply_invincible,
                        "TREE": self.apply_tree}
        self.updateLeftProb()
        self.updateRightProb()
        self.groups = [game.zipBird,game.allsprites]
        for each in self.groups:
            each.add(self)
        #use getSpecial() to determine if you're going to have a special bird
        #splice images and do stuff
        #actually make the thing show up

    def update(self):
        #CHECK COORDINATES to see if you need to draw it
        if not self.stationary:
            self.fly()

    def getSpecial(self):
        total = sum(prob_dict.values())
        on_right = random.random() >= 0.5
        probs = self.right_prob_dict if on_right else self.left_prob_dict
        special_rand = random.uniform(0, total)
        for item in probs.items():
            if special_rand < item[1]:
                break
            else:
                special_rand -= item[1]
        return item[0], on_right #returns string of bird type and boolean whether it's on the right side

    def updateLeftProb(self):
        #YOUR CODE HERE
        pass

    def updateRightProb(self):
        #YOUR CODE HERE
        pass

    def fly(self):
        """move the bird across the screen, and bounce at the ends"""
        newpos = self.rect.move((self.move, 0))
        if not self.area.contains(newpos):
            if self.rect.left < self.area.left or \
                    self.rect.right > self.area.right:
                self.move = -self.move
                newpos = self.rect.move((self.move, 0))
        self.rect = newpos

    def load_spliced_image(self, bird, length):#TODO: bird is a string, length is length of image
        #YOUR CODE HERE
        return Load.load_image(bird)


    def apply_effect(self):
        self.bird_type, on_right = self.getSpecial
        self.special_marker = self.rect.right - self.bird_size[0] if self.on_right else self.rect.left + self.bird_size[0] #position of the end of special bird block
        self.effect_dict[self.bird_type](on_right)

    def apply_fatso(self, on_right):
        if on_right:
            length_eaten = Game.right_bound - self.special_marker # TODO: margin
            self.rect.right = self.special_marker - length_eaten
        else:
            length_eaten = self.special_marker - Game.left_bound # TODO: margin
            self.rect.left = self.special_marker + length_eaten
        self.splice_image(length_eaten, on_right, True)

    def apply_squiddy(self): #TODO: Black screen for some time
        #YOUR CODE HERE
        pass

    def apply_invincible(self): #TODO: make a long block
        #YOUR CODE HERE
        pass

    def apply_tree(self):
        if self.on_right:
            length_built = Game.right_bound - self.rect.right
            self.rect.right += length_built
        else:
            length_built = self.rect.left - Game.left_bound
            self.rect.left -= length_built
        self.splice_image(length_built, on_right, False)

    def edit_image(self, length, on_right, splicing = True): #TODO: splice to add/delete part of the image
        #YOUR CODE HERE
        return Load.load_image('scooter.png', -1, length)
        pass
