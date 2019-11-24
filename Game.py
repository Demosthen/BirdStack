import os, sys
import pygame
from pygame.locals import *
from MurderedBird import *
from Load import *
from ZippedBird import *
class Game:
    def __init__(self, screensize = (468,468)):
        self.bird_density = "placeholder"#TODO: fill this in
        self.score = 0
        self.left_bound = 0 #top layer left_bound
        self.right_bound = 0 #top layer right_bound
        self.murders = {"BIRDIE": 0,
                        "FATSO": 0,
                        "SQUIDDY": 0,
                        "INVINCIBLE": 0,
                        "TREE": 0}
        self.used = {"BIRDIE": 0,
                        "FATSO": 0,
                        "SQUIDDY": 0,
                        "INVINCIBLE": 0,
                        "TREE": 0}
        pygame.init()
        self.screen = pygame.display.set_mode(screensize)
        pygame.display.set_caption("BIRD STACK")
        self.bigSurface = 0 # TODO: initialize big surface
        self.screenPos = ("placeholder", "placeholder")#TODO: fill this in
        self.background = pygame.Surface(self.screen.get_size())
        self.background = self.background.convert()
        self.background.fill((250,250,250))
        if pygame.font:
            font = pygame.font.Font(None, 36)
            text = font.render("STACK THE BIRDSSSSSSSS", 1, (10, 10, 10))
            textpos = text.get_rect(centerx=self.background.get_width()/2)
            self.background.blit(text, textpos)
        self.screen.blit(self.background, (0,0)) # TODO: pass area Rect to display only part of it
        pygame.display.flip()
        self.allsprites = pygame.sprite.RenderUpdates()
        self.towerSprites = pygame.sprite.RenderUpdates()
        self.clock = pygame.time.Clock()
        #TODO: add GUI BUTTONS (PLAY/PAUSE, SCORE, RESTART)

    def place(self):#TODO:
        #YOUR CODE HERE
        pass

    def gameEnded(self):#TODO:
        #YOUR CODE HERE
        pass

    def run(self):
        while 1:
            self.clock.tick(60)
            for event in pygame.event.get():
                if event.type == QUIT:
                    return
                elif event.type == KEYDOWN and event.key == K_ESCAPE:
                    return
                elif event.type == MOUSEBUTTONDOWN:
                    pass
                elif event.type == MOUSEBUTTONUP:
                    self.place() #TODO: fill in any parameters
            self.allsprites.update()
            dir = self.allsprites.draw(self.screen) #TODO: ONLY DRAW ONES ONSCREEN BY SUBCLASSING GROUP
            # TODO: draw to bigsurface, not screen
            pygame.display.update(dir)#TODO: replace with blit from bigsurface

            self.allsprites.clear(self.screen,self.background)
