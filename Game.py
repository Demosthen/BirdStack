import os, sys
import pygame
from pygame.locals import *
from MurderedBird import *
from Load import *
from ZippedBird import *
from CustomGroup import *

class Game:
    def __init__(self, screensize = (468,468)):
        self.bird_density = "placeholder"
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
        self.gui_sprites = { "PAUSE_PLAY" : "scooter.png",
                            "RESTART" : "scooter.png" }
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
            score = font.render("Score"+ str(self.score), True, (10, 10, 10))
            scorepos = text.get_rect(topright = (100,100))#this is unfinished
            self.background.blit(text, textpos)
        self.screen_height = 0 #height of bottom of screen
        self.bigSurface.blit(self.background, self.calcScreenRect()) # TODO: pass area Rect to display only part of it
        self.screen.blit(self.bigSurface, (0,0), area = self.calcScreenRect())
        pygame.display.flip()
        self.tolerance = 20# TODO: ADJUST LATER
        self.allsprites = pygame.sprite.RenderUpdates()
        self.murdered = pygame.sprite.RenderUpdates()
        self.tower = CustomGroup()
        self.zipBird = pygame.sprite.GroupSingle()
        self.gui = pygame.sprite.RenderUpdates()
        self.clock = pygame.time.Clock()
        #TODO: initialize with ZippedBird base
        #TODO: add GUI BUTTONS (PLAY/PAUSE, SCORE, RESTART)
        #TODO: actually make the zippedbird when you start the game
        #self.flock = ZippedBird(self, (100,100)) #TODO: please change this

    def calcScreenRect(self):
        return Rect(0, self.screen_height, self.screen.get_width(), self.screen_height+self.screen.get_height())

    def translateRect(self, rect):
        screenRect = self.calcScreenRect()
        return Rect(rect.left, rect.top + screenRect.top, rect.right, rect.bottom + screenRect.bottom)



    def place(self):#TODO:
        #YOUR CODE HERE
        #check the position of the zipped bird, compare with the tower left and right bounds, resize+move to tower group, generate extra birds to toss if needed (and specials)
        #check if there are special birds there that do stuff and do their effect
        bird_width = Bird.bird_size[0]
        if abs(self.right_bound - self.flock.rect.right) <= self.tolerance: #move it over if within certain tolerance
            self.flock.rect.move(self.right_bound - self.flock.rect.right, 0)
        elif abs(self.left_bound - self.flock.rect.left) <= self.tolerance:
            self.flock.rect.move(self.left_bound - self.flock.rect.left, 0)
        self.flock.stationary = True

        if (self.right_bound - self.flock.rect.right > 0.4*bird_width): #change to whatever fraction of the thing counts as a bird
            for i in range((self.right_bound - self.flock.rect.right)//bird_width):
                self.deadbirdsprites.add(MurderedBird((self.flock.rect.right - bird_width*i), self.flock.rect.y))
                #TODO: check if there's a special in there so that you generate a dead one of those
                pass
        if (self.flock.rect.left - self.left_bound > 0.4*bird_width): #change to whatever fraction of the thing counts as a bird
            for i in range((self.flock.rect.left - self.right_bound)//bird_width):
                self.deadbirdsprites.add(MurderedBird((self.flock.rect.left + bird_width*i), self.flock.rect.y))
                pass

        self.right_bound = self.flock.rect.right
        self.left_bound = self.flock.rect.left
        #TODO: move it to the tower group
        #TODO: do specials


        pass

    def check_GUI(self): #pause/play, restart; sprites, will get added into allsprites
        pass

    def endGame(self):#TODO: do the downward scroll, generate the dead bird pile, etc
        #YOUR CODE HERE
        pass

    def run(self):
        scrolling = False
        while play:
            self.clock.tick(60)
            move = True
            pos_y = max([each.rect.y for each in self.tower.sprites()]) + self.tower[0].bird_size[1]
            self.zipBird.add(ZippedBird(self,(0, pos_y)))
            if move:
                self.zipBird[0].fly()
            #else:
                #place, splice, drop here
                #update screen accordingly
                #check if game has ended
            self.check_GUI()
            cursor_pos = mouse.get_pos()
            #cursor_rect = Rect(cursor_pos[0]-1,cursor_pos[1]+1,2,2)
            for event in pygame.event.get():
                if event.type == QUIT:
                    return
                elif event.type == KEYDOWN and event.key == K_ESCAPE:
                    return
                elif event.type == KEYDOWN and event.key == K_s:
                    scrolling = True
                elif event.type == KEYUP and event.key == K_s:
                    scrolling = False
                #elif event.type == MOUSEBUTTONDOWN:
                    #self.allsprites.add(Bird())
                elif event.type == MOUSEBUTTONUP:
                    for sprite in self.allsprites.sprites():
                        sprite.dropping = True
                elif event.type == MOUSEBUTTONDOWN and not any([each.collidepoint(cursor_pos) for each in self.gui.sprites()]):
                    move = False


            if scrolling:
                self.screen_height -= 1
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
