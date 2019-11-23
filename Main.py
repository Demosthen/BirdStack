import os, sys
import pygame
from pygame.locals import *
from Bird import Bird
from Load import *

if not pygame.font: print('Warning, fonts disabled')
if not pygame.mixer: print('Warning, sound disabled')

def run():
    pygame.init()
    screen = pygame.display.set_mode((468,468))
    pygame.display.set_caption("BIRD STACK")
    background = pygame.Surface(screen.get_size())
    background = background.convert()
    background.fill((250,250,250))
    if pygame.font:
        font = pygame.font.Font(None, 36)
        text = font.render("STACK THE BIRDSSSSSSSS", 1, (10, 10, 10))
        textpos = text.get_rect(centerx=background.get_width()/2)
        background.blit(text, textpos)
    screen.blit(background, (0,0))
    pygame.display.flip()
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
        #pygame.display.flip()
run()
