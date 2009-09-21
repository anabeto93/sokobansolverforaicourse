'''
Created on Sep 1, 2009

@author: zagnut
'''

import pygame
from pygame.locals import *
import time
import threading
import os
import math

def get_full_path(relative_path):
        return os.path.dirname(os.path.dirname(os.path.abspath( __file__ ))) + relative_path

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
                point = self.get_map_point(i,j)
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
    
    def get_map_point(self, x, y):
        try:
            return self.textfile[y+1][x]
        except:
            return ' '
                
    def get_object_position(self, type):
        for x in xrange(self.width):
            for y in xrange(self.height):
                if self.get_map_point(x, y) == type:
                    return (x, y)
        return None
                
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

class Node():
    def __init__(self, point, parent = None, score = None, cost = None, heuristics = None): 
        self.parent = parent
        self.point = point
        self.score = score
    
    def __eq__(self, other):
        return (self.point[0] == other.point[0] and self.point[1] == other.point[1])
        
        
class AStarSearch():
    def __init__(self, map):
        self.map = map
        self.open_list = []
        self.closed_list = []

    def set_goal(self, node):
        self.goal = node
    
    def set_starting_position(self, node):
        self.node_start = node
    
    def __get_node_cost(self, node_current, node_to_cost):
        x_curr = node_current.point[0]
        y_curr = node_current.point[1]
        x_cost = node_to_cost.point[0]
        y_cost = node_to_cost.point[1]        
        return math.sqrt(abs(x_cost - x_curr)**2 + abs(y_cost - y_curr)**2)
    
    def __get_node_heuristic(self, node_goal, node_to_heuristic):
        x_goal = node_goal.point[0]
        y_goal = node_goal.point[1]
        x_heu = node_to_heuristic.point[0]
        y_heu = node_to_heuristic.point[1]        
        return math.sqrt(abs(x_heu - x_goal)**2 + abs(y_heu - y_goal)**2)        
        
    def __get_surrounding_nodes(self, node):
        x = node.point[0]
        y = node.point[1]
        
        #Finding the following points:
        points = []
        #North
        points.append((x, y + 1))
        #West
        points.append((x - 1, y))
        #East
        points.append((x + 1, y))
        #South
        points.append((x, y - 1))

        nodes = []
        for point in points:
            type = self.map.get_map_point(point[0], point[1])
            if type == '.' or type == 'G':
                nodes.append(Node(point, node))   
        return nodes
    
    def __score_nodes(self, node_current, surrounding_nodes):
        for node in surrounding_nodes:
            node.cost = self.__get_node_cost(node_current, node)
            node.heuristic = self.__get_node_heuristic(self.goal, node)
            node.score = node.cost + node.heuristic
    
    def __score_compare(self, node_a, node_b):
        if node_a.score > node_b.score:
            return 1
        elif node_a.score == node_b.score:
            return 0
        else:
            return -1
        
    def __is_node_in_list(self, node_to_check, node_list):
        for i, node in enumerate(node_list):
            if node == node_to_check:
                return i
        return False
    
    def do_search(self):
        goal_reached = False
        open_list_empty = False
        self.open_list.append(self.node_start)
        
        while not (goal_reached or open_list_empty):
            node_current = self.open_list[0]
            self.closed_list.append(node_current)
            self.open_list.remove(node_current)
            surrounding_nodes = self.__get_surrounding_nodes(node_current)
            self.__score_nodes(node_current, surrounding_nodes)
            for node in surrounding_nodes:
                i = self.__is_node_in_list(node, self.open_list)
                if i != False:
                    if node.cost < self.open_list[i].cost:
                        self.open_list[i].cost = node.cost
                        self.open_list[i].heuristic = node.heuristic
                        self.open_list[i].parent = node.parent
                if not self.__is_node_in_list(node, self.closed_list):
                    self.open_list.append(node)
                    #Check to see if it was the goal node
                    if node == self.goal:
                        self.closed_list.append(node)
                        goal_reached = True
                        
            if len(self.open_list) == 0:
                print 'Could not reach goal'
                open_list_empty = True
                
            self.open_list.sort(cmp = self.__score_compare)
    
        if goal_reached:
            for step in self.closed_list:
                print step.point
                self.map.man[0].x = step.point[0]
                self.map.man[0].y = step.point[1]
                time.sleep(0.6)
                
        self.open_list = []
        self.closed_list = []
        time.sleep(1)
            
def main_temp():
    x = Movement(MovementPhysical(), MovementVirtual())
    x.move_up()
    raw_input()
    
def main_temp2():
    pygame.display.set_mode()
    soko_map = Map(get_full_path('/rsc/mymap.txt'))
    search = AStarSearch(soko_map)
    
    goal = (1, 2)
    start = soko_map.get_object_position('M')
    
    tusch = Painter(soko_map)
    tusch.start()
    
    search.set_goal(Node(goal))
    search.set_starting_position(Node(start))
    search.do_search()
    
    search.set_goal(Node((8,7)))
    search.set_starting_position(Node(goal))
    search.do_search()
    #raw_input()
    
if __name__ == '__main__':
    main_temp2()