import pygame
import pymunk
from Load import *
import Game
numb_killed = 0
GRAVITY = 1000
class MurderedBird(pygame.sprite.Sprite):
    move = 3
    bird_size = (50,50)
    mass = 100

    image_dict = {"BIRDIE": "new_dead_birdie.png",
                    "FATSO": "new_dead_fatso.png",
                    "SQUIDDY": "new_dead_squidbird.png",
                    "INVINCIBLE": "new_dead_invincible.png",
                    "TREE": "new_dead_tree.png"}


    def __init__(self, game, startPos, type, to_b_or_not_2_b = False):
        #need add type
        pygame.sprite.Sprite.__init__(self)
        self.to_b_or_not_2_b = to_b_or_not_2_b
        self.groups = [game.allsprites,game.murdered]
        self.image, self.rect = load_image(self.image_dict[type], -1, self.bird_size)
        screen = pygame.display.get_surface()
        self.final_drawn = False
        #keep track of how many killed, how many types killed?
        self.game = game
        self.rect.center = self.game.translatePoint(startPos)
        self.area = screen.get_rect()
        self.onScreen = True
        self.moment = pymunk.moment_for_circle(self.mass, 0, max(self.bird_size)/2, (0,0))
        self.body = pymunk.Body(self.mass, self.moment)
        self.body.position = self.rect.center
        self.shape = pymunk.Circle(self.body, max(self.bird_size)/2, (0,0))
        self.shape.elasticity = 1
        self.friction = 0
        self.game.space.add(self.body, self.shape)
        for each in self.groups:
            each.add(self)

    def update(self):
        global numb_killed
        self.rect.center = self.body.position
        if not self.to_b_or_not_2_b:
            area = self.game.calcScreenRect()
            if self.rect.top >= area.bottom:
                numb_killed+=1
                print("DEAD!", numb_killed)
                self.game.space.remove(self.shape, self.body)
                self.kill()
                del self
        #self.drop()


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
