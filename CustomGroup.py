import pygame
from pygame.locals import *
from SquidInk import *
#this i tower
class CustomGroup(pygame.sprite.RenderUpdates):#TODO: ALL OF IT
    def __init__(self, game):
        pygame.sprite.RenderUpdates.__init__(self)
        self.game = game
        #YOUR CODE HERE


    def draw(self, surface):
       spritedict = self.spritedict
       surface_blit = surface.blit
       dirty = self.lostsprites
       self.lostsprites = []
       dirty_append = dirty.append
       screenRect = self.game.calcScreenRect()
       cnt = 0
       def draw_sprite(s):
           nonlocal cnt
           if not s.onScreen:
               if not s.final_drawn:# draw one last time so its previous sprite on screen gets cleared
                   s.final_drawn = True
               else:
                   return
           cnt+=1
           r = spritedict[s]
           newrect = surface_blit(s.image, s.rect)
           if r:
               if newrect.colliderect(r):
                   dirty_append(newrect.union(r))
               else:
                   dirty_append(newrect)
                   dirty_append(r)
           else:
               dirty_append(newrect)
           spritedict[s] = newrect
       for s in self.sprites():
           if type(s) != SquidInk:
               draw_sprite(s)
       for s in self.sprites():#draw squidink sprites last
           if type(s) == SquidInk:
               draw_sprite(s)
       return dirty

    def clear(self, surface, bgd):
        """erase the previous position of all sprites
        Group.clear(surface, bgd): return list of Rects
        Clears the area under every drawn sprite in the group. The bgd
        argument should be Surface which is the same dimensions as the
        screen surface. The bgd could also be a function which accepts
        the given surface and the area to be cleared as arguments.
        Returns a list of all cleared Rects.
        """
        clearedRects = []
        if callable(bgd):
            for r in self.lostsprites:
                bgd(surface, r)
                clearedRects.append(r)
            for r in self.spritedict.values():
                if r:
                    bgd(surface, r)
                    clearedRects.append(r)
        else:
            surface_blit = surface.blit
            for r in self.lostsprites:
                surface_blit(bgd, r, r)
                clearedRects.append(r)
            for r in self.spritedict.values():
                if r:
                    clearedRects.append(r)
                    surface_blit(bgd, r, r)
        return clearedRects
