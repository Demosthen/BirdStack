import pygame
import Load
class Denero(pygame.sprite.Sprite):
    def __init__(self, game, size):
        pygame.sprite.Sprite.__init__(self)
        self.image, self.rect = Load.load_image("denero.jpg", -1, size)
        self.game = game
        game.allsprites.add(self)
        self.rect.bottom = self.game.bigSurface.get_rect().bottom
        self.rect.left = 0
        self.onScreen = True
