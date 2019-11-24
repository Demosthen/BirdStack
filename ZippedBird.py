import random
import os, sys
import pygame
from pygame.locals import *
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
        self.image, self.rect = load_spliced_image('scooter.png', -1, startPos)
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
        updateLeftProb()
        updateRightProb()
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
        for bird, prob in probs.values():
            if special_rand < prob:
                break
            else:
                special_rand -= prob
        return bird

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

    def load_spliced_image(self, bird, length):# bird is a string, length is length of image
        #YOUR CODE HERE
        pass
