import os, sys
import pygame
from pygame.locals import *

if not pygame.font: print('Warning, fonts disabled')
if not pygame.mixer: print('Warning, sound disabled')

gravity = 9

def load_image(name, colorkey=None, sizes = (50,50)):
    fullname = os.path.join('data', name)
    try:
        image = pygame.image.load(fullname)
        image = pygame.transform.scale(image, sizes)
    except pygame.error as message:
        print('Cannot load image:', name)
        raise SystemExit(message)
    image = image.convert()
    if colorkey is not None:
        if colorkey is -1:
            colorkey = image.get_at((0, 0))
        image.set_colorkey(colorkey, RLEACCEL)
    return image, image.get_rect()
def load_sound(name):
    class NoneSound:
        def play(self): pass
    if not pygame.mixer:
        return NoneSound()
    fullname = os.path.join('data', name)
    try:
        sound = pygame.mixer.Sound(fullname)
    except pygame.error as message:
        print('Cannot load sound:', wav)
        raise SystemExit(message)
    return sound

class Bird(pygame.sprite.Sprite):
    move = 9
    bird_size = (50,50)
    def __init__(self, startPos = (100,100)):
        pygame.sprite.Sprite.__init__(self)
        self.image, self.rect = load_image('scooter.png', -1, startPos)
        screen = pygame.display.get_surface()
        self.dropping = False
        self.stationary = False
        self.rect.center = startPos
        self.area = screen.get_rect()

    def update(self):
        if not self.stationary:
            if self.dropping:
                self.drop()
            else:
                self.fly()

    def fly(self):
        """move the bird across the screen, and turn at the ends"""
        newpos = self.rect.move((self.move, 0))
        if not self.area.contains(newpos):
            if self.rect.left < self.area.left or \
                    self.rect.right > self.area.right:
                self.move = -self.move
                newpos = self.rect.move((self.move, 0))
                self.image = pygame.transform.flip(self.image, 1, 0)
        self.rect = newpos

    def drop(self):
        """make the bird fall"""
        newpos = self.rect.move((0, gravity))
        self.rect = newpos
        if self.rect.top >= self.area.height:
            print("DEAD!")
            self.kill()


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
    allsprites = pygame.sprite.RenderPlain()
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
        screen.blit(background, (0,0))
        allsprites.draw(screen)
        pygame.display.flip()
run()
