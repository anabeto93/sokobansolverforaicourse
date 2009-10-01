'''
Created on Sep 1, 2009

@author: zagnut
'''

from pygame.locals import *
import random
import math
import os
import pygame
import threading
import time
import itertools
import copy

def get_full_path(relative_path):
        return os.path.dirname(os.path.dirname(os.path.abspath( __file__ ))) + relative_path

def benchmark(function):
    def wrap(*args):            
        time_start = time.time()
        function(*args)
        time_finish = time.time()
        print('Time taken for ' + function.__name__ + ': ' + str((time_finish - time_start) * 1000) + ' ms')
    return wrap

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
        print('moving')
    
class MovementVirtual(Mover):   
    def __init__(self, soko_map):
        self.map_layout = soko_map
    
    def move_up(self):
        jewel = self.map_layout.check_for_jewel(self.map_layout.man[0].x,self.map_layout.man[0].y-1)
        if jewel != None:
            jewel.y = jewel.y-1
        self.map_layout.man[0].y = self.map_layout.man[0].y-1
        self.map_layout.man[0].img = self.map_layout.man[0].img_up
        print('moving up')
    
    def move_down(self):
        jewel = self.map_layout.check_for_jewel(self.map_layout.man[0].x,self.map_layout.man[0].y+1)
        if jewel != None:
            jewel.y = jewel.y+1
        self.map_layout.man[0].y = self.map_layout.man[0].y+1
        self.map_layout.man[0].img = self.map_layout.man[0].img_down
        print('moving down')
    
    def move_left(self):
        jewel = self.map_layout.check_for_jewel(self.map_layout.man[0].x-1,self.map_layout.man[0].y)
        if jewel != None:
            jewel.x = jewel.x-1
        self.map_layout.man[0].x = self.map_layout.man[0].x-1
        self.map_layout.man[0].img = self.map_layout.man[0].img_left
        print('moving left')
    
    def move_right(self):
        jewel = self.map_layout.check_for_jewel(self.map_layout.man[0].x+1,self.map_layout.man[0].y)
        if jewel != None:
            jewel.x = jewel.x+1
        self.map_layout.man[0].x = self.map_layout.man[0].x+1
        self.map_layout.man[0].img = self.map_layout.man[0].img_right
        print('moving right')
        
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
        self.width = None
        self.height = None
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
                
    def get_object_position(self, square_type):
        for x in xrange(self.width):
            for y in xrange(self.height):
                if self.get_map_point(x, y) == square_type:
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
    def __init__(self, soko_map):
        threading.Thread.__init__(self)
        self.daemon = True
        pygame.init() 
        self.map_layout = soko_map
        self.background = None
        self.screen = pygame.display.set_mode((self.map_layout.man[0].img.get_width()*self.map_layout.width, self.map_layout.man[0].img.get_height()*self.map_layout.height))
        pygame.display.set_caption('SokoHero')
        
    def draw(self):
        self.background = pygame.Surface(self.screen.get_size())
        self.background = self.background.convert()
        self.background.fill((121, 121, 121, 0))
        self.screen.blit(self.background, (0,0))
        sprites = []
        sprites.extend(self.map_layout.bricks)
        sprites.extend(self.map_layout.goals)
        sprites.extend(self.map_layout.jewels)
        sprites.extend(self.map_layout.man)
        for sprite in sprites:
            self.screen.blit(sprite.img, (sprite.x*sprite.img.get_width(),sprite.y*sprite.img.get_height()))
        pygame.display.flip()
        
    def run(self):
        while True:
            self.draw()
            time.sleep(0.1)

class Node():
    def __init__(self, point, parent = None, score = None, cost = None, heuristics = None): 
        self.parent = parent
        self.point = point
        self.score = score
    
    def __eq__(self, other):
        return (self.point[0] == other.point[0] and self.point[1] == other.point[1])
              

            
class SokoState():
    def __init__(self, soko_map, parent = None):
        self.jewels = []
        self.goals = []
        self.bricks = []
        self.man = None
        self.map_layout = [['']*soko_map.height for i in xrange(soko_map.width)]
        self.cost = 0
        self.parent = None
        
        #Take a copy of the map_layout
        for i in xrange(soko_map.width):
            for j in xrange(soko_map.height):
                point = soko_map.get_map_point(i, j)
                self.map_layout[i][j] = point
                if point == 'X':
                    self.bricks.append((i, j))
                elif point == 'J':
                    self.jewels.append((i, j))
                elif point == 'M':
                    self.man = (i, j)
                elif point == 'G':
                    self.goals.append((i, j))
    
    def update_jewel_position(self, jewel, new_position):
        index = self.jewels.index(jewel)
        self.jewels[index] = new_position
        self.map_layout[jewel[0]][jewel[1]] = '.'
        self.map_layout[new_position[0]][new_position[1]] = 'J'
    
    def update_man_position(self, new_position):
        self.map_layout[self.man[0]][self.man[1]] = '.'
        self.map_layout[new_position[0]][new_position[1]] = 'M'
        self.man = new_position
        
    def get_heuristic(self):
        #=======================================================================
        # We use manhatten distance
        #=======================================================================
        heurist = 0
        minimum_dist = 0
        for jewel in self.jewels:
            if jewel in self.goals:
                continue
            minimum_dist = 0
            for goal in self.goals:
                dist = abs(goal[0] - jewel[0]) + abs(goal[1] - jewel[0])
                if dist < minimum_dist:
                    minimum_dist = dist 
                heurist += minimum_dist
    def is_goal_state(self):
        for jewel in self.jewels:
            if jewel not in self.goals:
                return False
        return True
    
    def __eq__(self, other):
        equal = True
        for jewel in self.jewels:
            if not jewel in other.jewels:
                equal = False
                break
        return equal
    
class AStarSearch():
    def __init__(self, soko_state):
        self.map = soko_state
        self.open_list = []
        self.closed_list = []
        self.nodes_to_goal = []
        self.goal_reached = False
        
    def set_goal_node(self, node):
        self.open_list = []
        self.closed_list = []
        self.nodes_to_goal = []
        self.goal_reached = False
        self.node_goal = node
    
    def set_starting_node(self, node):
        self.open_list = []
        self.closed_list = []
        self.nodes_to_goal = []
        self.goal_reached = False
        self.node_start = node
    
    def _get_node_cost(self, node_current, node_to_cost):
        x_curr = node_current.point[0]
        y_curr = node_current.point[1]
        x_cost = node_to_cost.point[0]
        y_cost = node_to_cost.point[1]        
        return abs(x_cost - x_curr) + abs(y_cost - y_curr)
    
    def _get_node_heuristic(self, node_goal, node_to_heuristic):
        x_goal = node_goal.point[0]
        y_goal = node_goal.point[1]
        x_heu = node_to_heuristic.point[0]
        y_heu = node_to_heuristic.point[1]        
        return abs(x_heu - x_goal) + abs(y_heu - y_goal)        
        
    def _get_surrounding_nodes(self, node):
        x = node.point[0]
        y = node.point[1]
    
        nodes = []
        points = []
        points.append((x - 1, y))
        points.append((x + 1, y))
        points.append((x, y + 1))
        points.append((x, y - 1))
        for point in points:
            square_type = self.map.map_layout[point[0]][point[1]]
            if square_type == '.' or square_type == 'G':
                nodes.append(Node(point, node))
        return nodes
    
    def _score_nodes(self, node_current, surrounding_nodes, node_end):
        for node in surrounding_nodes:
            node.cost = self._get_node_cost(node_current, node)
            node.heuristic = self._get_node_heuristic(node_end, node)
            node.score = node.cost + node.heuristic
    
    def _score_compare(self, node_a, node_b):
        if node_a.score > node_b.score:
            return 1
        elif node_a.score == node_b.score:
            return 0
        else:
            return -1
    
    def _construct_path_to_goal(self, node_start, node_end):
        node = node_end
        while node != node_start:
            self.nodes_to_goal.insert(0, node)
            node = node.parent
    
    def set_search_for_type(self, search_for_type):
        self.search_for_type = search_for_type
        
    #@benchmark  
    def do_search(self, node_start, node_end):
        self.nodes_to_goal = []
        self.open_list = []
        self.closed_list = []
        self.goal_reached = False
        
        open_list_empty = False
        self.open_list.append(node_start)
        
        while not (self.goal_reached or open_list_empty):
            self.open_list.sort(cmp = self._score_compare)
            node_current = self.open_list[0]
            self.closed_list.append(node_current)
            self.open_list.remove(node_current)
            surrounding_nodes = self._get_surrounding_nodes(node_current)
            self._score_nodes(node_current, surrounding_nodes, node_end)
            
            for node in surrounding_nodes:
                if node in self.open_list:
                    i = self.open_list.index(node)
                    if node.cost < self.open_list[i].cost:
                        self.open_list[i] = node
                else:        
                    if node not in self.closed_list:
                        self.open_list.append(node)
                        if node == node_end:
                            node_end.parent = node.parent
                            self.closed_list.append(node)
                            self._construct_path_to_goal(node_start, node_end)
                            return True
                        
            if len(self.open_list) == 0:
                #print 'Could not reach goal
                return False
            
class SokoSolver():
    def __init__(self, soko_map):
        self.initial_soko_state = SokoState(soko_map)
        self.player_move_searcher = AStarSearch(self.initial_soko_state)
        self.open_list = []
        self.closed_list = []
        
    def is_move_possible(self, soko_state, jewel, direction):
        if direction == 'U':
            if soko_state.map_layout[jewel[0]][jewel[1] - 1] == '.' or soko_state.map_layout[jewel[0]][jewel[1] - 1] == 'G':
                return True
        elif direction == 'D':
            if soko_state.map_layout[jewel[0]][jewel[1] + 1] == '.' or soko_state.map_layout[jewel[0]][jewel[1] + 1] == 'G':
                return True
        elif direction == 'L':
            if soko_state.map_layout[jewel[0] - 1][jewel[1]] == '.' or soko_state.map_layout[jewel[0] - 1][jewel[1]] == 'G':
                return True
        elif direction == 'R':
            if soko_state.map_layout[jewel[0] + 1][jewel[1]] == '.' or soko_state.map_layout[jewel[0] + 1][jewel[1]] == 'G':
                return True 
    
    def is_state_possible(self, state):
        for jewel in state.jewels:
            if jewel in state.goals:
                return True
            left_square = state.map_layout[jewel[0]][jewel[1] - 1]
            right_square = state.map_layout[jewel[0]][jewel[1] + 1]
            up_square = state.map_layout[jewel[0] - 1][jewel[1]]
            down_square = state.map_layout[jewel[0] + 1][jewel[1]]
            if (left_square == 'X' or right_square == 'X') and (up_square == 'X' or down_square == 'X'):
                return False 
            
    def expand(self, soko_state):
        for jewel in soko_state.jewels:
            
            state = copy.deepcopy(soko_state)
            if self.is_move_possible(state, jewel, 'U'):
                if self.player_move_searcher.do_search(Node(state.man), Node((jewel[0], jewel[1] + 1))):
                    state.update_jewel_position(jewel, (jewel[0], jewel[1] - 1))
                    state.update_man_position((jewel[0], jewel[1] + 1))
                    if self.is_state_possible(state):
                        state.cost += state.get_heuristics()
                        state.cost += len(self.player_move_searcher.nodes_to_goal)
                        state.parent = soko_state
                        if state in self.open_list:
                            index = self.open_list.index(state)
                            if state.cost < self.open_list[index].cost:
                                self.open_list[index] = state
                        else:
                            if state not in self.closed_list:
                                self.open_list.append(state)
                                
            state = copy.deepcopy(soko_state)       
            if self.is_move_possible(soko_state, jewel, 'D'):
                if self.player_move_searcher.do_search(Node(soko_state.man), Node((jewel[0], jewel[1] - 1))):
                    state.update_jewel_position(jewel, (jewel[0], jewel[1] + 1))
                    state.update_man_position((jewel[0], jewel[1] - 1))
                    if self.is_state_possible(state):
                        state.cost += state.get_heuristics()
                        state.cost += len(self.player_move_searcher.nodes_to_goal)
                        state.parent = soko_state
                        if state in self.open_list:
                            index = self.open_list.index(state)
                            if state.cost < self.open_list[index].cost:
                                self.open_list[index] = state
                        else:
                            if state not in self.closed_list:
                                self.open_list.append(state)
                        
            state = copy.deepcopy(soko_state)          
            if self.is_move_possible(soko_state, jewel, 'L'):
                if self.player_move_searcher.do_search(Node(soko_state.man), Node((jewel[0] + 1, jewel[1]))):
                    state.update_jewel_position(jewel, (jewel[0], jewel[1] - 1))
                    state.update_man_position((jewel[0] + 1, jewel[1]))
                    if self.is_state_possible(state):
                        state.cost += state.get_heuristics()
                        state.cost += len(self.player_move_searcher.nodes_to_goal)
                        state.parent = soko_state
                        if state in self.open_list:
                            index = self.open_list.index(state)
                            if state.cost < self.open_list[index].cost:
                                self.open_list[index] = state
                        else:
                            if state not in self.closed_list:
                                self.open_list.append(state)
                        
            state = copy.deepcopy(soko_state)              
            if self.is_move_possible(soko_state, jewel, 'R'):
                if self.player_move_searcher.do_search(Node(soko_state.man), Node((jewel[0] - 1, jewel[1]))):
                    state.update_jewel_position(jewel, (jewel[0], jewel[1] + 1))
                    state.update_man_position((jewel[0] - 1, jewel[1]))
                    if self.is_state_possible(state):
                        state.cost += state.get_heuristics()
                        state.cost += len(self.player_move_searcher.nodes_to_goal)
                        state.parent = soko_state
                        if state in self.open_list:
                            index = self.open_list.index(state)
                            if state.cost < self.open_list[index].cost:
                                self.open_list[index] = state
                        else:
                            if state not in self.closed_list:
                                self.open_list.append(state)           
    
    def score_compare(self, state_a, state_b):
        if state_a.score > state_b.score:
            return 1
        elif state_a.score == state_b.score:
            return 0
        else:
            return -1
        
    def solve(self):
        self.open_list = []
        self.open_list.append(self.initial_soko_state)
        tries = 0
        while len(self.open_list) > 0:
            tries += 1
            if tries % 1000 == 0:
                print('Nr. of tries: ' + str(tries))
            self.open_list.sort(cmp = self.score_compare)
            top_state = self.open_list[0]
            self.closed_list.append(top_state)
            if not top_state.is_goal_state():
                self.expand(top_state)
            else:
                'Solved the puzzle!'
                break
        
def main_5():
    pygame.display.set_mode()
    soko_map = Map(get_full_path('/rsc/map2.txt'))
    solver = SokoSolver(soko_map)
    tusch = Painter(soko_map)
    tusch.start()    
    print('Going to work')
    if solver.solve():
        print('Solved')
    else:
        print('Could not solve puzzle')
            

if __name__ == '__main__':
    main_5()