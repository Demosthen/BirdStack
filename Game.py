import os, sys
import pygame
from pygame.locals import *
from Bird import *
from Load import *
from ZippedBird import *
class Game:
    def __init__(self, screensize = (468,468)):
        self.bird_density = "placeholder"
        self.score = 0
        self.left_bound = 0
        self.right_bound = 0
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
        self.background = pygame.Surface(self.screen.get_size())
        self.background = self.background.convert()
        self.background.fill((250,250,250))
        if pygame.font:
            font = pygame.font.Font(None, 36)
            text = font.render("STACK THE BIRDSSSSSSSS", 1, (10, 10, 10))
            textpos = text.get_rect(centerx=background.get_width()/2)
            self.background.blit(text, textpos)
        self.screen.blit(background, (0,0))
        pygame.display.flip()
        self.allsprites = pygame.sprite.RenderUpdates
    def run():
        allsprites = pygame.sprite.RenderUpdates()
        clock = pygame.time.Clock()
        while 1:
            clock.tick(60)
            for event in pygame.event.get():
                if event.type == QUIT:
                    return
                elif event.type == KEYDOWN and event.key == K_ESCAPE:
                    return
                elif event.type == MOUSEBUTTONDOWN:
                    allsprites.add(Bird())
                elif event.type == MOUSEBUTTONUP:
                    for sprite in allsprites.sprites():
                        sprite.dropping = True
            allsprites.update()
            print(len(allsprites.sprites()))
            dir = allsprites.draw(screen)
            pygame.display.update(dir)
            allsprites.clear(screen,background)
