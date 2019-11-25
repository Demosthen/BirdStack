from Game import *
from Load import *

class GuiSprites(pygame.sprite.Sprite):
    """docstring for SquidInk."""
    image_dict = {"PAUSE": "new_pause.png",
                    "PLAY": "new_play.png",
                    "RESTART": "new_restart.png",
                    "TITLE": "new_title.png",
                    "SCORE": "new_score.png",
                    "FINAL_SCORE":"new_final_score.png",
                    "BIRDS_KILLED": "new_bird_count.png",
                    "FINAL_RESTART": "new_final_restart.png",
                    "THANKS": "new_thanks.png",
                    "CREDITS": "new_credit_birds.png"}

    image_size = {"PAUSE": (20, 20),
                    "PLAY": (20, 20),
                    "RESTART": (20, 20),
                    "TITLE": (400,50),
                    "SCORE": (100,30),
                    "FINAL_SCORE": (400,50),
                    "BIRDS_KILLED": (300,200),
                    "FINAL_RESTART": (400,50),
                    "THANKS": (300,50),
                    "CREDITS": (400,100)}

    gui_display = {"PAUSE": (400,80),
                    "PLAY": (400,80),
                    "RESTART": (420,80),
                    "TITLE": (234,30),
                    "SCORE": (420,60),
                    "FINAL_SCORE": (234,70),
                    "BIRDS_KILLED": (234,180),
                    "FINAL_RESTART": (234,290),
                    "THANKS": (234,330),
                    "CREDITS": (234,390)}

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
        self.onScreen =True
        self.group = [game.allsprites,game.gui]
        for each in self.group:
            each.add(self)
        self.font = pygame.font.SysFont("Calibri", 24)
        if self.type == "SCORE":
            textSurf = self.font.render(str(self.game.score), 1, (255,223,0))
            self.image.blit (textSurf,  ( 70, 8) )
        if self.type == "FINAL_SCORE":
            textSurf = self.font.render(str(self.game.score), 1, (255,223,0))
            self.image.blit (textSurf,  ( 350, 20) )
        if self.type == "BIRDS_KILLED":
            textSurf = self.font.render(str(sum(self.game.murders.values())), 1, (0,0,0)) #total
            self.image.blit (textSurf,  ( 250, 20) )
            textSurf = self.font.render(str(self.game.murders["BIRDIE"]), 1, (0,0,0))
            self.image.blit (textSurf,  ( 250, 50) )
            textSurf = self.font.render(str(self.game.murders["FATSO"]), 1, (0,0,0))
            self.image.blit (textSurf,  ( 250, 80) )
            textSurf = self.font.render(str(self.game.murders["SQUIDDY"]), 1, (0,0,0))
            self.image.blit (textSurf,  ( 250, 110) )
            textSurf = self.font.render(str(self.game.murders["INVINCIBLE"]), 1, (0,0,0))
            self.image.blit (textSurf,  ( 250, 140) )
            textSurf = self.font.render(str(self.game.murders["TREE"]), 1, (0,0,0))
            self.image.blit (textSurf,  ( 250, 170) )


    def update(self):
        if self.type == "SCORE":
            self.kill()
            new = GuiSprites(self.game,"SCORE")
        screen = pygame.display.get_surface()
        startPos = self.gui_display[self.type]
        self.rect.center = self.game.translatePoint(startPos)
