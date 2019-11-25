from Game import *
from Load import *

class GuiSprites(pygame.sprite.Sprite):
    """docstring for SquidInk."""
    image_dict = {"PAUSE": "new_pause.png",
                    "PLAY": "new_play.png",
                    "RESTART": "new_restart.png",
                    "TITLE": "new_title.png",
                    "SCORE": "new_score.png"}

    image_size = {"PAUSE": (20, 20),
                    "PLAY": (20, 20),
                    "RESTART": (20, 20),
                    "TITLE": (400,50),
                    "SCORE": (100,30)}

    gui_display = {"PAUSE": (400,80),
                    "PLAY": (400,80),
                    "RESTART": (420,80),
                    "TITLE": (234,30),
                    "SCORE": (420,60)}

    def __init__(self, game, type):
        pygame.sprite.Sprite.__init__(self)
        self.type = type
        self.game = game
        self.onScreen = True

        #self.get_position(type)
        type_image = self.image_dict[self.type]
        type_size = self.image_size[self.type]
        self.image, self.rect = load_image(type_image, -1, type_size)
        screen = pygame.display.get_surface()
        startPos = self.gui_display[self.type]
        self.rect.center = self.game.translatePoint(startPos)

        self.group = [game.gui,game.allsprites]
        for each in self.group:
            each.add(self)


    def update(self):
        screen = pygame.display.get_surface()
        startPos = self.gui_display[self.type]
        self.rect.center = self.game.translatePoint(startPos)
