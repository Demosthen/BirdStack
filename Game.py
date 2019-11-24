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
        self.screen = pygame.display.set_mode(screensize)
        self.left_bound = self.screen.get_width()//2-100 #top layer left_bound
        self.right_bound = self.screen.get_width()//2+100 #top layer right_bound
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
        pygame.display.set_caption("BIRD STACK")
        self.bigSurface = pygame.Surface((self.screen.get_width(), self.screen.get_height() * 20))
        self.background = pygame.Surface(self.bigSurface.get_size())
        self.background = self.background.convert()
        self.background.fill((250,250,250))
        if pygame.font:
            font = pygame.font.Font(None, 36)
            text = font.render("STACK THE BIRDSSSSSSSS", 1, (10, 10, 10))
            textpos = text.get_rect(centerx=self.background.get_width()/2)
            score = font.render("Score"+ str(self.score), True, (10, 10, 10))
            scorepos = text.get_rect(topright = (100,100))#this is unfinished
            self.background.blit(text, textpos)
        self.screen_height = 0
        self.bigSurface.blit(self.background, (0,0)) # TODO: pass area Rect to display only part of it
        self.screen.blit(self.bigSurface, (0,0), area = self.calcScreenRect())
        pygame.display.flip()
        self.tolerance = 10# TODO: ADJUST LATER
        self.allsprites = pygame.sprite.RenderUpdates()
        self.murdered = pygame.sprite.RenderUpdates()
        self.tower = CustomGroup()
        self.zipBird = pygame.sprite.GroupSingle()
        self.gui = pygame.sprite.RenderUpdates()
        self.clock = pygame.time.Clock()
        self.scroll = 5 # amount it scrolls each frame
        self.squiddy_clock = pygame.time.Clock()
        #TODO: initialize with ZippedBird base
        #TODO: add GUI BUTTONS (PLAY/PAUSE, SCORE, RESTART)
        #TODO: actually make the zippedbird when you start the game
        #self.flock = ZippedBird(self, (100,100)) #TODO: please change this

    def calcScreenRect(self):# calculate the screen's rect within bigSurface
        return Rect(0, self.bigSurface.get_height()- self.screen.get_height() -self.screen_height, self.screen.get_width(), self.bigSurface.get_height() - self.screen_height)

    def translateRect(self, rect):#translate a rect from screen coordinates to bigSurface coordinates
        screenRect = self.calcScreenRect()
        return Rect(rect.left, rect.top + screenRect.top, rect.right, rect.bottom + screenRect.top)

    def fromBiggie(self, rect):# translate a rect from bigSurface coordinates to
        screenRect = self.calcScreenRect()
        return Rect(rect.left, rect.top - screenRect.top, rect.right, rect.bottom - screenRect.top)

    def translatePoint(self,tuple):# translate a point from screen coordinates to bigSurface coordinates
        return (tuple[0], tuple[1] + self.bigSurface.get_height()- self.screen.get_height() -self.screen_height)

    def fromBiggiePoint(self, tuple):# translate a rect from bigSurface coordinates to
        screenRect = self.calcScreenRect()
        return (tuple[0], tuple[1] - (self.bigSurface.get_height()- self.screen.get_height() -self.screen_height))


    def place(self):#TODO:
        #YOUR CODE HERE
        #check if there are special birds there that do stuff and do their effect
        flock = self.zipBird.sprites()[0]
        bird_width = MurderedBird.bird_size[0]
        left = flock.rect.left
        right = flock.rect.right
        if abs(self.right_bound - right) <= self.tolerance: #move it over if within certain tolerance
            right += self.right_bound - flock.rect.right
            left += self.right_bound - flock.rect.right
            # flock.rect.move(self.right_bound - flock.rect.right, 0)
        elif abs(self.left_bound - left) <= self.tolerance:
            right += self.left_bound - flock.rect.left
            left += self.left_bound - flock.rect.left
            # flock.rect.move(self.left_bound - flock.rect.left, 0)
        flock.stationary = True


        x = (min(right, self.right_bound) + max(left, self.left_bound))/2
        #x = flock.rect.centerx
        y = flock.rect.centery
        length = min(right, self.right_bound) - max(left, self.left_bound) #resize
        if length<5:
            return "u suck u lose"
        #FIX MUDRDERED BIRDS
        # if (self.right_bound - flock.rect.right > 0.4*bird_width): #change to whatever fraction of the thing counts as a bird
        #     for i in range((self.right_bound - flock.rect.right)//bird_width):
        #         self.murdered.add(MurderedBird(self,(flock.rect.right - bird_width*i, flock.rect.y)))
        #         #TODO: check if there's a special in there so that you generate a dead one of those
        #
        # if (flock.rect.left - self.left_bound > 0.4*bird_width): #change to whatever fraction of the thing counts as a bird
        #     for i in range((flock.rect.left - self.right_bound)//bird_width):
        #         self.murdered.add(MurderedBird(self,(flock.rect.left + bird_width*i, flock.rect.y)))

        #TODO: do special effects

        flock.place(self.left_bound, self.right_bound, length)
        flock.relocate(self.fromBiggiePoint((x,y)))
        flock.stationary = True
        self.tower.add(flock)

        self.right_bound = min(right, self.right_bound) #resets left and right bounds
        self.left_bound = max(left, self.left_bound)

        #self.towerSprites.add(self.flock)
        #flock.kill()
        #print(x,y)
        #print(length) #LENGTH IS OFF, FIX

        #new = ZippedBird(self, length,self.fromBiggiePoint((x, y)))
        #new.stationary = True
        #self.tower.add(new)


        moving = ZippedBird(self,length,self.fromBiggiePoint((200, y-50)))
        print(len(self.tower.sprites()),len(self.murdered.sprites()), len(self.allsprites.sprites()) )



    """if (some key down):
        place self.flock/moving/whatever you called it
        check to see if the game has ended
            if so, self.endGame()
        create a newZippedBird"""


    def check_GUI(self): #pause/play, restart; sprites, will get added into allsprites
        pass

    def endGame(self):#TODO: do the downward scroll, generate the dead bird pile, etc
        #YOUR CODE HERE
        pass

    def run(self):
        length = self.right_bound-self.left_bound
        scrolling = False
        play = True
        base = ZippedBird(self,length,(self.screen.get_width()/2,self.screen.get_height()-100))
        base.stationary = True
        self.tower.add(base)
        #self.allsprites.add(base)
        pos_y = min([each.rect.y for each in self.tower.sprites()]) -25#self.tower.sprites()[0].bird_size[1]
        moving = ZippedBird(self,length,self.fromBiggiePoint((self.screen.get_width()/2, pos_y)))
        while play:
            stopped = False
            #print(len(self.zipBird.sprites()))
            #print(len(self.allsprites.sprites()))
            self.clock.tick(60)
            #else:
                #place, splice, drop here
                #update screen accordingly
                #check if game has ended
            self.check_GUI()
            cursor_pos = pygame.mouse.get_pos()
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
                    #self.allsprites.add(MurderedBird(self))
                #elif event.type == MOUSEBUTTONUP:
                    #for sprite in self.allsprites.sprites():
                        #sprite.dropping = True
                elif event.type == MOUSEBUTTONDOWN and not any([each.collidepoint(cursor_pos) for each in self.gui.sprites()]):
                    stopped = True

            if stopped:
                if self.place():
                    self.endGame()
                else:
                    self.check_GUI()




            if scrolling:
                self.screen_height += self.scroll
            self.allsprites.update()
            #self.bigSurface.blit(self.background, self.calcScreenRect()) # TODO: pass area Rect to display only part of it
            self.allsprites.clear(self.bigSurface,self.background)
            dir = self.allsprites.draw(self.bigSurface) #TODO: ONLY DRAW ONES ONSCREEN BY SUBCLASSING GROUP
            # TODO: draw to bigsurface, not screen
            screenRect = self.calcScreenRect()
            onScreen = [d for d in dir if screenRect.contains(d)]# only blit the ones on screen
            if scrolling:
                #self.screen_height += self.scroll# move up screen
                onScreen = [Rect(d.left - abs(self.scroll)*2, d.top - abs(self.scroll)*2, d.right+ abs(self.scroll)*2, d.bottom + abs(self.scroll)*2) for d in onScreen] # correct dirty rectangles
            #self.screen.blit(self.bigSurface, (0,0), screenRect)
            self.screen.blits([(self.bigSurface, self.fromBiggie(d), d) for d in onScreen])
            pygame.display.update([self.fromBiggie(d) for d in onScreen])
            #pygame.display.flip()
