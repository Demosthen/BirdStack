import random
import os, sys
import pygame
import Load
from pygame.locals import *
import Game
from SquidInk import *

class ZippedBird(pygame.sprite.Sprite):
    move = 3
    orig_move = 3
    bird_size = (50,50)
    image_dict = {"BIRDIE": "new_birdie.png",
                    "FATSO": "new_fatso.png",
                    "SQUIDDY": "new_squidbird.png",
                    "INVINCIBLE": "new_invincible.png",
                    "TREE": "new_tree.png"}
    need_append = {"BIRDIE": -1,# 1 if need to increase length, 0 if don't need to increase length
                    "FATSO": 1,
                    "SQUIDDY": 1,
                    "INVINCIBLE": 0,
                    "TREE": 0}


    def __init__(self, game, length,startPos = (250,100)):
        pygame.sprite.Sprite.__init__(self)
        self.length = length
        self.game = game
        self.move_right = 1
        self.left_prob_dict = {"BIRDIE": 5,
                        "FATSO": 1,
                        "SQUIDDY": 1,
                        "INVINCIBLE": 1,
                        "TREE": 1}
        self.right_prob_dict = {"BIRDIE": 5,
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
        if len(game.tower.sprites()) == 0:
            for key,val in self.left_prob_dict.items():
                if key == 'BIRDIE':
                    self.left_prob_dict[key] = 1
                else:
                    self.left_prob_dict[key] = 0
            for key,val in self.right_prob_dict.items():
                if key == 'BIRDIE':
                    self.right_prob_dict[key] = 1
                else:
                    self.right_prob_dict[key] = 0
        self.groups = [game.zipBird, game.allsprites]
        for each in self.groups:
            each.add(self)
        #use getSpecial() to determine if you're going to have a special bird
        self.bird_type, self.on_right = self.getSpecial()
        self.image, self.rect = self.edit_image( self.length, False)
        print(self.rect.height)
        screen = pygame.display.get_surface()
        self.stationary = False
        self.rect.center = self.game.translatePoint(startPos)
        self.ink_turn = 3
        self.margin = 25
        self.final_drawn = False
        self.area = screen.get_rect() # TODO: UPDATE THIS ACCORDING TO GAME SCREEN POSITION
        self.onScreen = True
        #splice images and do stuff
        #actually make the thing show up

    def update(self):
        #CHECK COORDINATES to see if you need to draw it
        self.onScreen = self.game.checkPointOnScreen(self.rect.topleft)
        if not self.stationary:
            self.fly()


    def place(self, left_bound, right_bound, length):
        if self.bird_type != 'BIRDIE':
            if self.on_right:
                special_right = self.rect.right
                special_left = self.rect.right - self.bird_size[0]
            else:
                special_right = self.rect.left + self.bird_size[0]
                special_left = self.rect.left
            if not((left_bound < special_left - self.game.tolerance and right_bound > special_right + self.game.tolerance) or
                (special_left < left_bound and special_right > right_bound)):
                print("BIRDIE!!", left_bound, special_left, right_bound, special_right)
                self.bird_type = "BIRDIE"
                self.image, self.rect = self.edit_image(length)
        self.resize(length)
        print("left:", self.rect.left, "right:", self.rect.right)



    def resize(self, newLength):
        new = pygame.transform.scale(self.image, (newLength, self.image.get_height()))
        self.image, self.rect = new, new.get_rect()
        self.length = newLength

    def relocate(self, newLoc):
        self.rect.center = self.game.translatePoint(newLoc)

    def getSpecial(self):
        if self.game.invincible:
            return "BIRDIE", True
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

    def updateLeftProb(self): #TREE, FATSO,INVINCIBLE, SQUIDDY
        #YOUR CODE HERE
        self.left_prob_dict["BIRDIE"] = 2
        if self.game.left_bound<50:
            self.left_prob_dict["TREE"] = 0
            self.left_prob_dict["FATSO"]+= 2
        elif self.game.left_bound > 234:
            self.left_prob_dict["TREE"] += 1
        if self.game.right_bound - self.game.left_bound > 100:
            self.left_prob_dict["SQUIDDY"]+=0.5
        else:
            self.left_prob_dict["SQUIDDY"]-=0.5
            self.left_prob_dict["INVINCIBLE"]+=1

        if self.game.right_bound - self.game.left_bound < self.bird_size[0]:
            for key, val in self.need_append.items():
                if val == 0:
                    self.left_prob_dict[key] = 0

    def updateRightProb(self):
        #YOUR CODE HERE
        if self.game.right_bound>418:
            self.right_prob_dict["TREE"] = 0
            self.right_prob_dict["FATSO"]+= 2
        elif self.game.right_bound < 234:
            self.right_prob_dict["TREE"] += 1
        if self.game.right_bound - self.game.left_bound > 100:
            self.right_prob_dict["SQUIDDY"]+=0.5
        else:
            self.right_prob_dict["SQUIDDY"]-=0.5
            self.right_prob_dict["INVINCIBLE"]+=1


        if self.game.right_bound - self.game.left_bound < self.bird_size[0]:
            for key, val in self.need_append.items():
                if val == 0:
                    self.right_prob_dict[key] = 0

    def fly(self):
        """move the bird across the screen, and bounce at the ends"""
        newpos = self.rect.move((self.move * self.move_right, 0))
        if not self.area.contains(newpos):
            if self.rect.left < self.area.left or \
                    self.rect.right > self.area.right:
                self.move_right = - self.move_right
                newpos = self.rect.move((self.move * self.move_right, 0))
        self.rect = newpos

    def apply_effect(self):
        self.special_marker = self.rect.right - self.bird_size[0] if self.on_right else self.rect.left + self.bird_size[0] #position of the end of special bird block
        print(self.special_marker, self.rect.left, self.rect.right)
        self.effect_dict[self.bird_type]()

    def apply_fatso(self):
        if self.on_right:
            self.length_eaten = self.rect.right - self.special_marker # TODO: margin
        else:
            self.length_eaten = self.special_marker - self.rect.left # TODO: margin
        self.bird_type = "BIRDIE"
        #print("pos:", self.rect.left, self.rect.right)
        print(self.length, self.length_eaten, self.length - 2 * self.length_eaten)
        if self.length - 2 * self.length_eaten > 0:
            self.length = self.length - 2 * self.length_eaten
            self.image,self.rect = self.edit_image(self.length, True)
            print("after pos:", self.rect.left, self.rect.right, self.length)
            self.bird_type = "FATSO"
        else:
            self.game.is_negative_length = True
            print("game over cuz length exceeds by ", self.length - 2 * self.length_eaten)

    def apply_squiddy(self):
        #Game.squiddy_clock = pygame.time.Clock()
        #Game.squiddy_clock.tick()

        ink = SquidInk(self.game, self.ink_turn)
        ink.update()

    def apply_invincible(self):\
        self.game.invincible = True

    def apply_tree(self):
        if self.on_right:
            print("right")
            self.length_built = self.rect.right - self.special_marker # TODO: margin
        else:
            print('left')
            self.length_built = self.special_marker - self.rect.left
        self.bird_type = "BIRDIE"
        self.length += self.length_built
        self.image,self.rect = self.edit_image(self.length, True)
        print("after pos:", self.rect.left, self.rect.right, self.length)
        self.bird_type = "TREE"


    def edit_image(self, length, splicing = True):
        #YOUR CODE HERE
        imgs = [0,0]
        if self.bird_type == "BIRDIE":
            img = self.make_long_img(Load.load_image("new_birdie.png", -1, self.bird_size)[0], length)[0]
            return img, img.get_rect()
        imgs[self.on_right] = Load.load_image(self.image_dict[self.bird_type], -1,self.bird_size)[0]
        #imgs[not self.on_right] = Load.load_image('new_birdie.png', -1, (length - self.bird_size[0] * (not self.need_append[self.bird_type]),self.bird_size[1]))[0]
        imgs[not self.on_right] = self.make_long_img(Load.load_image("new_birdie.png", -1, self.bird_size)[0], (length - self.bird_size[0] * (not self.need_append[self.bird_type])))[0]
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

    def make_long_img(self, img, length):
        num_imgs = length // img.get_width()
        leftover = int(length % img.get_width())
        full_list = []
        for i in range(num_imgs):
            full_list.append(img)
        leftoverSurf = pygame.Surface(img.get_size())
        leftoverSurf.blit(img, (0,0))
        leftoverSurf = pygame.transform.scale(leftoverSurf, (leftover, img.get_height()))
        print(leftoverSurf.get_size())
        full_list.append(leftoverSurf)
        return self.splice_image(full_list)
