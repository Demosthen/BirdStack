import random
import os, sys
import pygame
import Load
from pygame.locals import *
import Game
class ZippedBird(pygame.sprite.Sprite):
    move = 3
    bird_size = (50,50)
    image_dict = {"BIRDIE": "scooter.png",
                    "FATSO": "fatso.jpg",
                    "SQUIDDY": "scooter.png",
                    "INVINCIBLE": "invincible.jpg",
                    "TREE": "tree.png"}
    need_append = {"BIRDIE": -1,# 1 if need to increase length, 0 if don't need to increase length
                    "FATSO": 1,
                    "SQUIDDY": 1,
                    "INVINCIBLE": 0,
                    "TREE": 0}


    def __init__(self, game, length,startPos = (250,100)):
        pygame.sprite.Sprite.__init__(self)
        self.length = length
        self.game = game

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
        self.groups = [game.zipBird, game.allsprites]
        for each in self.groups:
            each.add(self)
        #use getSpecial() to determine if you're going to have a special bird
        self.bird_type, self.on_right = self.getSpecial()
        self.image, self.rect = self.edit_image( self.length, False)
        screen = pygame.display.get_surface()
        self.stationary = False
        self.rect.center = self.game.translatePoint(startPos)
        self.ink_turn = 3
        self.margin = 25
        self.area = screen.get_rect() # TODO: UPDATE THIS ACCORDING TO GAME SCREEN POSITION
        #self.length = game.right_bound - game.left_bound
        if self.bird_type == "BIRDIE":
            pass
        elif self.bird_type == "FATSO":
            pass
        elif self.bird_type == "SQUIDDY":
            pass
        elif self.bird_type == "INVINCIBLE":
            pass
        elif self.bird_type == "TREE":
            pass


        #splice images and do stuff
        #actually make the thing show up

    def update(self):
        #CHECK COORDINATES to see if you need to draw it
        if not self.stationary:
            self.fly()
    def place(self, left_bound, right_bound):
        if self.bird_type != "BIRDIE":
            if self.on_right:
                special_right = self.rect.right
                special_left = self.rect.right - self.bird_size[0]
            else:
                special_right = self.rect.left + self.bird_size[0]
                special_left = self.rect.left
            if left_bound >= special_left or right_bound <= special_right:
                self.bird_type = "BIRDIE"
        self.resize(right_bound - left_bound)



    def resize(self, newLength):
        self.image, self.rect = self.edit_image(newLength)

    def relocate(self, newLoc):
        self.rect.center = self.game.translatePoint(newLoc)

    def getSpecial(self):
        on_right = random.random() >= 0.5
        probs = self.right_prob_dict if on_right else self.left_prob_dict
        total = sum(probs.values())
        special_rand = random.uniform(0, total)
        for item in probs.items():
            if special_rand < item[1]:
                break
            else:
                special_rand -= item[1]
        return item[0], on_right #returns string of bird type and boolean whether it's on the right side

    """
    conditions for creating each of the bird types:
    all specials    : must have enough length to display a full bird
                      must not be in invincibility mode (different image?)
    TREE:           : game.left_bound > somenumber, game.right_bound < somenumber
    FATSO:          : must be < max screen length - one bird length
    INVINCIBLE:     :
    SQUIDDY:        : must be < max screen length - one bird length

    """

    def updateLeftProb(self):
        #YOUR CODE HERE
        if self.game.right_bound - self.game.left_bound < self.bird_size[0]:
            for key, val in self.need_append.items():
                if val == 0:
                    self.left_prob_dict[key] = 0
        pass

    def updateRightProb(self):
        #YOUR CODE HERE
        if self.game.right_bound - self.game.left_bound < self.bird_size[0]:
            for key, val in self.need_append.items():
                if val == 0:
                    self.right_prob_dict[key] = 0
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
        self.bird_type, on_right = self.getSpecial()
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

    def apply_squiddy(self):
        #Game.squiddy_clock = pygame.time.Clock()
        #Game.squiddy_clock.tick()

        SquidInk(self.game, self.ink_turn)


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

    def edit_image(self, length, splicing = True):
        #YOUR CODE HERE
        imgs = [0,0]
        if self.bird_type == "BIRDIE":
            img = Load.load_image('scooter.png', -1, (length,self.bird_size[1]))[0]
            return img, img.get_rect()
        imgs[self.on_right] = Load.load_image(self.image_dict[self.bird_type], -1,self.bird_size)[0]
        imgs[not self.on_right] = Load.load_image('scooter.png', -1, (length - self.bird_size[0] * (not self.need_append[self.bird_type]),self.bird_size[1]))[0]
        return self.splice_image(imgs)

    def splice_image(self, imgs):#concatenates a list of images into one surface
        total_width = sum([i.get_width() for i in imgs])
        max_height = max([i.get_height() for i in imgs])
        new_img = pygame.Surface((total_width, max_height))
        pos = 0
        for i in imgs:
            new_img.blit(i, (pos, 0))
            pos += i.get_width()
        return new_img, new_img.get_rect()
