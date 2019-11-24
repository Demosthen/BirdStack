import os, sys
import pygame
from pygame.locals import *
from Bird import *
from Load import *
from ZippedBird import *
from CustomGroup import *

class Game:
    def __init__(self, screensize = (468,468)):
        self.bird_density = "placeholder"
        self.score = 0
        self.left_bound = 0 #bound of top layer of tower
        self.right_bound = 0 #bound of top layer of tower
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
        self.background = pygame.Surface(self.screen.get_size())
        self.background = self.background.convert()
        self.background.fill((250,250,250))
        if pygame.font:
            font = pygame.font.Font(None, 36)
            text = font.render("STACK THE BIRDSSSSSSSS", 1, (10, 10, 10))
            textpos = text.get_rect(centerx=self.background.get_width()/2)
            score = font.render("Score"+ self.score, True, (10, 10, 10))
            scorepos = text.get_rect(top_right = (self.screensize[],))#this is unfinished
            self.background.blit(text, textpos)
            self.background.blit(score,scorepos)
        #put GUI sprites here
        self.screen.blit(self.background, (0,0))
        pygame.display.flip()
        self.allsprites = pygame.sprite.RenderUpdates()
        self.murdered = pygame.sprite.RenderUpdates()
        self.tower = CustomGroup()
        self.zipBird = pygame.sprite.GroupSingle()
        self.gui = pygame.sprite.RenderUpdates()
        self.clock = pygame.time.Clock()

    def check_GUI(self): #pause/play, restart; sprites, will get added into allsprites
        pass

    def run(self):
        while play:
            move = True
            pos_y = max[each.rect.y for each in self.tower] + self.tower[0].bird_size[1]
            self.zipBird.add(ZippedBird(self,(0, pos_y)))
            while move:
                self.zipBird[0].fly()
                self.check_GUI()
                cursor_pos = mouse.get_pos()
                #cursor_rect = Rect(cursor_pos[0]-1,cursor_pos[1]+1,2,2)
                if event.type = MOUSEBUTTONDOWN and (not any[each.collidepoint(cursor_pos) for each in self.gui]):
                    move = False
            #place, splice, drop here
            #update screen accordingly
            #check if game has ended

        while 1:
            self.clock.tick(60)
            for event in pygame.event.get():
                if event.type == QUIT:
                    return
                elif event.type == KEYDOWN and event.key == K_ESCAPE:
                    return
                elif event.type == MOUSEBUTTONDOWN:
                    self.allsprites.add(Bird())
                elif event.type == MOUSEBUTTONUP:
                    for sprite in self.allsprites.sprites():
                        sprite.dropping = True
            self.allsprites.update()
            dir = self.allsprites.draw(self.screen)
            pygame.display.update(dir)
            self.allsprites.clear(self.screen,self.background)
