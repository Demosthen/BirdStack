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
        self.bigSurface = pygame.Surface((self.screen.get_width(), self.screen.get_height() * 20))
        self.screenPos = ("placeholder", "placeholder")#TODO: fill this in
        self.background = pygame.Surface(self.screen.get_size())
        self.background = self.background.convert()
        self.background.fill((250,250,250))
        if pygame.font:
            font = pygame.font.Font(None, 36)
            text = font.render("STACK THE BIRDSSSSSSSS", 1, (10, 10, 10))
            textpos = text.get_rect(centerx=self.background.get_width()/2)
            self.background.blit(text, textpos)
        self.screen_height = 0 #height of bottom of screen
        self.bigSurface.blit(self.background, self.calcScreenRect()) # TODO: pass area Rect to display only part of it
        self.screen.blit(self.bigSurface, (0,0), area = self.calcScreenRect())
        pygame.display.flip()
        self.allsprites = pygame.sprite.RenderUpdates()
        self.towerSprites = pygame.sprite.RenderUpdates()
        self.clock = pygame.time.Clock()
        #TODO: initialize with ZippedBird base
        #TODO: add GUI BUTTONS (PLAY/PAUSE, SCORE, RESTART)
        #TODO: actually make the zippedbird when you start the game
        self.flock = ZippedBird(self, (100,100)) #TODO: please change this
    def calcScreenRect(self):
        return Rect(0, self.screen_height, self.screen.get_width(), self.screen_height+self.screen.get_height())
    def translateRect(self, rect):
        screenRect = self.calcScreenRect()
        return Rect(rect.left, rect.top + screenRect.top, rect.right, rect.bottom + screenRect.bottom)



    def place(self):#TODO:
        #YOUR CODE HERE
        #check the position of the zipped bird, compare with the tower left and right bounds, resize+move to tower group, generate extra birds to toss if needed (and specials)
        #check if there are special birds there that do stuff and do their effect
        if abs(self.right_bound - self.flock.rect.right) <= self.tolerance: #move it over if within certain tolerance
            self.flock.rect.move(self.right_bound - self.flock.rect.right, 0)
        elif abs(self.left_bound - self.flock.rect.left) <= self.tolerance:
            self.flock.rect.move(self.left_bound - self.flock.rect.left, 0)
        self.flock.stationary = True

        if (self.right_bound - self.flock.rect.right > 0.4*bird_width): #change to whatever fraction of the thing counts as a bird
            for i in range((self.right_bound - self.flock.rect.right)//bird_width):
                #TODO: make a murderedbird
                #ALSO: check if there's a special in there so that you generate a dead one of those
                pass
        if (self.flock.rect.left - self.left_bound > 0.4*bird_width): #change to whatever fraction of the thing counts as a bird
            for i in range((self.flock.rect.left - self.right_bound)//bird_width):
                #TODO: make a murderedbird
                pass

        self.right_bound = self.flock.rect.right
        self.left_bound = self.flock.rect.left
        #TODO: move it to the tower group
        #TODO: do specials
        #TODO: check if gameEnded
        #TODO: move screen up, then create new flock

        pass

    def gameEnded(self):#TODO:
        #YOUR CODE HERE
        pass

    def run(self):
        scrolling = False
        while 1:
            self.clock.tick(60)
            for event in pygame.event.get():
                if event.type == QUIT:
                    return
                elif event.type == KEYDOWN and event.key == K_ESCAPE:
                    return
                elif event.type == KEYDOWN and event.key == K_s:
                    scrolling = True
                elif event.type == KEYUP and event.key == K_s:
                    scrolling = False
                elif event.type == MOUSEBUTTONDOWN:
                    self.allsprites.add(Bird())
                elif event.type == MOUSEBUTTONUP:
                    for sprite in self.allsprites.sprites():
                        sprite.dropping = True
                    self.place() #TODO: fill in any parameters

            if scrolling:
                self.screen_height += 1
            self.allsprites.update()
            dir = self.allsprites.draw(self.bigSurface) #TODO: ONLY DRAW ONES ONSCREEN BY SUBCLASSING GROUP
            # TODO: draw to bigsurface, not screen
            screenRect = self.calcScreenRect()
            onScreen = [d for d in dir if screenRect.contains(d)]
            self.screen.blit(self.bigSurface, (0,0), screenRect)
            #self.screen.blits((self.bigSurface, (d.left, d.top - screenRect.top), d) for d in onScreen)
            self.allsprites.clear(self.bigSurface,self.background)
            #pygame.display.update([self.translateRect(d) for d in onScreen])#TODO: replace with blit from bigsurface
            pygame.display.flip()
