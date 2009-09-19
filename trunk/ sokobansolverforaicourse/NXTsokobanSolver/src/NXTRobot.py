'''
Created on Sep 1, 2009

@author: zagnut
'''

import pygame
from pygame.locals import *
import time
import threading
import os
    
class Movement():
    def __init__(self, physicalMover, virtualMover):       
        self.physicalMover = physicalMover
        self.virtualMover = virtualMover
        
    def move_up(self):
        if self.physicalMover != None:
            self.physicalMover.move_up()
        if self.virtualMover != None:
            self.virtualMover.move_up()
    
    def move_left(self):
        if self.physicalMover != None:
            self.physicalMover.move_left()
        if self.virtualMover != None:
            self.virtualMover.move_left()     
    
    def move_right(self):
        if self.physicalMover != None:
            self.physicalMover.move_right()
        if self.virtualMover != None:
            self.virtualMover.move_right()   
    
    def move_down(self):
        if self.physicalMover != None:
            self.physicalMover.move_down()
        if self.virtualMover != None:
            self.virtualMover.move_down()   

class Mover():
    def move_up(self):
        raise "not implemented"
    
    def move_down(self):
        raise "not implemented"
    
    def move_left(self):
        raise "not implemented"
    
    def move_right(self):
        raise "not implemented"

    
class MovementPhysical(Mover):
    def move_up(self):
        print 'moving'
    
class MovementVirtual(Mover):   
    def __init__(self, map):
        self.map = map
    
    def move_up(self):
        jewel = self.map.check_for_jewel(self.map.man[0].x,self.map.man[0].y-1)
        if jewel != None:
            jewel.y = jewel.y-1
        self.map.man[0].y = self.map.man[0].y-1
        self.map.man[0].img = self.map.man[0].img_up
        print 'moving up'
    
    def move_down(self):
        jewel = self.map.check_for_jewel(self.map.man[0].x,self.map.man[0].y+1)
        if jewel != None:
            jewel.y = jewel.y+1
        self.map.man[0].y = self.map.man[0].y+1
        self.map.man[0].img = self.map.man[0].img_down
        print 'moving down'
    
    def move_left(self):
        jewel = self.map.check_for_jewel(self.map.man[0].x-1,self.map.man[0].y)
        if jewel != None:
            jewel.x = jewel.x-1
        self.map.man[0].x = self.map.man[0].x-1
        self.map.man[0].img = self.map.man[0].img_left
        print 'moving left'
    
    def move_right(self):
        jewel = self.map.check_for_jewel(self.map.man[0].x+1,self.map.man[0].y)
        if jewel != None:
            jewel.x = jewel.x+1
        self.map.man[0].x = self.map.man[0].x+1
        self.map.man[0].img = self.map.man[0].img_right
        print 'moving right'
        
class Sprite():
    def __init__(self, x,y,img, img_up=None, img_down=None, img_left=None, img_right=None):
        self.img = pygame.image.load(img).convert_alpha()
        self.x = x
        self.y = y
        if img_up != None:
            self.img_up = pygame.image.load(img_up).convert_alpha()
            self.img_down = pygame.image.load(img_down).convert_alpha()
            self.img_left = pygame.image.load(img_left).convert_alpha()
            self.img_right = pygame.image.load(img_right).convert_alpha()
    
class Map():
    def __init__(self, maptext):
        self.textfile = [t.replace('\n', '') for t in open(maptext)]
        self._getMapProperties()
        #print 'WIDTH:', self.width, 'HEIGHT:', self.height, 'GOALS:', self.goals
        #for t in self.textfile:
        #    print t
        self.man = []
        self.jewels = []
        self.goals = []
        self.bricks = []
        for i in xrange(self.width):
            for j in xrange(self.height):
                point = self._get_map_point(i,j)
                if point == 'X':
                    self.bricks.append(Sprite(i,j, get_full_path('/gfx/brick.bmp')))
                elif point == 'J':
                    self.jewels.append(Sprite(i,j, get_full_path('/gfx/jewel.bmp')))
                elif point == 'M':
                    self.man.append(Sprite(i,j, get_full_path('/gfx/man.bmp'),  get_full_path('/gfx/man_up.bmp'), get_full_path('/gfx/man_down.bmp'), get_full_path('/gfx/man_left.bmp'), get_full_path('/gfx/man_right.bmp')))
                elif point == 'G':
                    self.goals.append(Sprite(i,j, get_full_path('/gfx/goal.bmp')))

    def _getMapProperties(self):
        values = self.textfile[0].split(' ')
        self.width = int(values[0])
        self.height = int(values[1])
        self.goals = int(values[2])
    
    def _get_map_point(self, x, y):
        try:
            return self.textfile[y+1][x]
        except:
            return ' '

    def check_for_obstacle(self, x, y):
        obstacle = self.check_for_brick(x,y)
        if obstacle == None:
            obstacle = self.check_for_jewel(x, y)
        return obstacle
    
    def check_for_jewel(self, x, y):
        for jewel in self.jewels:
            if jewel.y == y and jewel.x == x:
                return jewel
        return None
    def check_for_brick(self, x, y):
        for brick in self.bricks:
            if brick.y == y and brick.x == x:
                return brick
        return None
    
    def check_for_goal(self, x, y):
        for goal in self.goals:
            if goal.y == y and goal.x == x:
                return goal
        return None

class Painter(threading.Thread):
    def __init__(self, map):
        threading.Thread.__init__(self)
        self.daemon = True
        pygame.init() 
        self.map = map
        self.screen = pygame.display.set_mode((self.map.man[0].img.get_width()*self.map.width, self.map.man[0].img.get_height()*self.map.height))
        pygame.display.set_caption('SokoHero')
        
    def draw(self):
        self.background = pygame.Surface(self.screen.get_size())
        self.background = self.background.convert()
        self.background.fill((121, 121, 121, 0))
        self.screen.blit(self.background, (0,0))
        sprites = []
        sprites.extend(self.map.bricks)
        sprites.extend(self.map.goals)
        sprites.extend(self.map.jewels)
        sprites.extend(self.map.man)
        for sprite in sprites:
            self.screen.blit(sprite.img, (sprite.x*sprite.img.get_width(),sprite.y*sprite.img.get_height()))
        pygame.display.flip()
        
    def run(self):
        while True:
            self.draw()
            time.sleep(0.5)
def get_full_path(relative_path):
        return os.path.dirname(os.path.dirname(os.path.abspath( __file__ ))) + relative_path
        
def main_temp():
    x = Movement(MovementPhysical(), MovementVirtual())
    x.move_up()
    raw_input()
    
def main_temp2():
    pygame.display.set_mode()

    t = Map(get_full_path('/rsc/mymap.txt'))
    x = Movement(None, MovementVirtual(t))
    tusch = Painter(t)
    tusch.start()
 #   tusch.draw()
    time.sleep(3)
    x.move_right()
    time.sleep(1)
    x.move_right()
    time.sleep(1)
    x.move_right()
    time.sleep(1)
    x.move_down()
 #   tusch.draw()
    raw_input()
    
if __name__ == '__main__':
    main_temp2()