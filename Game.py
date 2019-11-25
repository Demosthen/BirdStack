import os, sys
import pygame
from pygame.locals import *
from MurderedBird import *
from Load import *
from ZippedBird import *
from CustomGroup import *
from GuiSprites import *

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
        self.paused = False
        self.screen_height = 0
        # if pygame.font:
        #     font = pygame.font.Font(None, 36)
        #     text = font.render("STACK THE BIRDSSSSSSSS", 1, (10, 10, 10))
        #     textpos = text.get_rect()
        #     textpos.center = self.translatePoint((self.screen.get_width()/2,10))
        #     score = font.render("Score: "+ str(self.score), True, (10, 10, 10))
        #     scorepos = score.get_rect()#this is unfinished
        #     scorepos.topright = self.translatePoint((screensize[0]-25,25))
        #     self.background.blit(text, textpos)
            #self.background.blit(score, scorepos)
        self.bigSurface.blit(self.background, (0,0)) # TODO: pass area Rect to display only part of it
        self.screen.blit(self.bigSurface, (0,0), area = self.calcScreenRect())
        pygame.display.flip()
        self.tolerance = 10# TODO: ADJUST LATER
        self.allsprites = CustomGroup(self)
        self.murdered = CustomGroup(self)
        self.tower = CustomGroup(self)
        self.zipBird = pygame.sprite.GroupSingle()
        self.gui = CustomGroup(self)
        self.clock = pygame.time.Clock()
        self.is_negative_length = False
        self.final_drawn = False
        self.scroll = 5 # amount it scrolls each frame
        #self.squiddy_time = 1500
        self.turns = 0
        self.invincible = False

    def calcScreenRect(self):# calculate the screen's rect within bigSurface
        return Rect(0, self.bigSurface.get_height()- self.screen.get_height() -self.screen_height, self.screen.get_width(), self.screen.get_height())

    def translateRect(self, rect):#translate a rect from screen coordinates to bigSurface coordinates
        screenRect = self.calcScreenRect()
        return Rect(rect.left, rect.top + screenRect.top, rect.width, rect.height)

    def fromBiggie(self, rect):# translate a rect from bigSurface coordinates to
        screenRect = self.calcScreenRect()
        return Rect(rect.left, rect.top - screenRect.top, rect.width, rect.height)

    def translatePoint(self,tuple):# translate a point from screen coordinates to bigSurface coordinates
        return (tuple[0], tuple[1] + self.bigSurface.get_height()- self.screen.get_height() -self.screen_height)

    def fromBiggiePoint(self, tuple):# translate a rect from bigSurface coordinates to
        screenRect = self.calcScreenRect()
        return (tuple[0], tuple[1] - (self.bigSurface.get_height()- self.screen.get_height() -self.screen_height))

    def checkPointOnScreen(self, pt):
        screenRect = self.calcScreenRect()
        return pt[1] < screenRect.bottom

    def place(self):#TODO:
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


        #FIX MUDRDERED BIRDS
        if (right - self.right_bound > 0.2*bird_width): #change to whatever fraction of the thing counts as a bird
            for i in range(round((right - self.right_bound)/bird_width)):
                print(i)
                self.murdered.add(MurderedBird(self,self.fromBiggiePoint((right+20*(i+1), flock.rect.y))))
                #TODO: check if there's a special in there so that you generate a dead one of those
        if (self.left_bound - left > 0.2*bird_width): #change to whatever fraction of the thing counts as a bird
            for i in range(round((self.left_bound - left)//bird_width)):
                print(i)
                self.murdered.add(MurderedBird(self,self.fromBiggiePoint((left-+20*(i+1), flock.rect.y))))

        length = min(right, self.right_bound) - max(left, self.left_bound) #resize

        print("placed:", flock.bird_type)
        flock.place(self.left_bound, self.right_bound, length)
        if flock.bird_type != "BIRDIE": #apply special effect if it's not normal bird
            flock.apply_effect()
        length = flock.length
        flock.relocate(self.fromBiggiePoint((x,y)))
        flock.stationary = True
        self.tower.add(flock)

        self.right_bound = min(right, self.right_bound) #resets left and right bounds
        self.left_bound = max(left, self.left_bound)
        if length < 5 or self.is_negative_length:
            flock.kill()
            return "u suck u lose"

        "handle apply_invincible"
        if self.invincible:
            moving = ZippedBird(self,468,self.fromBiggiePoint((200, y-50)))
            self.invincible = False
            print(moving.length)
        else:
            moving = ZippedBird(self,length,self.fromBiggiePoint((200, y-50)))
        print("bird_type: ", moving.bird_type)
        print(len(self.tower.sprites()),len(self.murdered.sprites()), len(self.allsprites.sprites()) )
        self.turns += 1
        print("turn: ", self.turns)


    """if (some key down):
        place self.flock/moving/whatever you called it
        check to see if the game has ended
            if so, self.endGame()
        create a newZippedBird"""


    def check_GUI(self,gui): #pause/play, restart; sprites, will get added into allsprites
        if gui.type == "PAUSE":
            gui.kill()
            new = GuiSprites(self, "PLAY")
            self.paused = True
        if gui.type == "PLAY":
            gui.kill()
            new = GuiSprites(self, "PAUSE")
            self.paused = False
        if gui.type == "RESTART":
            return "RESTART"

        #pass

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
        pause = GuiSprites(self,"PAUSE")
        restart = GuiSprites(self,"RESTART")
        title = GuiSprites(self,"TITLE")
        score = GuiSprites(self,"SCORE")
        while play:
            stopped = False
            #print(len(self.zipBird.sprites()))
            #print(len(self.allsprites.sprites()))
            self.clock.tick(60)
            #else:
                #place, splice, drop here
                #update screen accordingly
                #check if game has ended
            #self.check_GUI()
            cursor_pos = self.translatePoint(pygame.mouse.get_pos())
            #cursor_rect = Rect(cursor_pos[0]-1,cursor_pos[1]+1,2,2)
            pointers = [each.rect.collidepoint(cursor_pos) for each in self.gui.sprites()]
            for event in pygame.event.get():
                if event.type == QUIT:
                    return "END"
                elif event.type == KEYDOWN and event.key == K_ESCAPE:
                    return "END"
                elif event.type == KEYDOWN and event.key == K_s:
                    scrolling = True
                elif event.type == KEYUP and event.key == K_s:
                    scrolling = False
                #elif event.type == MOUSEBUTTONDOWN:
                    #self.allsprites.add(MurderedBird(self))
                #elif event.type == MOUSEBUTTONUP:
                    #for sprite in self.allsprites.sprites():
                        #sprite.dropping = True

                elif event.type == MOUSEBUTTONDOWN and not any(pointers): #there is no "play" sprite
                    stopped = True
                elif event.type == MOUSEBUTTONDOWN and any(pointers):
                    x = self.gui.sprites()[pointers.index(1)]
                    print(x.type)
                    if self.check_GUI(x) == "RESTART":
                        return "RESTART"

            if stopped:
                if self.place():
                    self.endGame()

            def displayGroup(group):
                group.update()
                #self.bigSurface.blit(self.background, self.calcScreenRect()) # TODO: pass area Rect to display only part of it
                cleared = group.clear(self.bigSurface,self.background)
                dir = group.draw(self.bigSurface) #TODO: ONLY DRAW ONES ONSCREEN BY SUBCLASSING GROUP
                # TODO: draw to bigsurface, not screen
                screenRect = self.calcScreenRect()
                onScreen = [d for d in dir if screenRect.contains(d)] + cleared# only blit the ones on screen
                if scrolling:
                    #self.screen_height += self.scroll# move up screen
                    onScreen = [Rect(d.left - abs(self.scroll)*2, d.top - abs(self.scroll)*2, d.right+ abs(self.scroll)*2, d.bottom + abs(self.scroll)*2) for d in onScreen] # correct dirty rectangles
                #self.screen.blit(self.bigSurface, (0,0), screenRect)
                self.screen.blits([(self.bigSurface, self.fromBiggie(d), d) for d in onScreen])
                pygame.display.update([self.fromBiggie(d) for d in onScreen])

            if self.paused:
                displayGroup(self.gui)
            else:
                #update score; code already above
                if scrolling:
                    self.screen_height += self.scroll
                displayGroup(self.allsprites)
                #pygame.display.flip()
