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
              
class AStarSearch():
    def __init__(self, soko_state):
        self.map = soko_state
        self.open_list = []
        self.closed_list = []
        self.nodes_to_goal = []
        self.goal_reached = False

        self.node_goal = None
        self.node_start = None
        self.search_for_type = None
        
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
        if self.search_for_type == 'G':
            #We can only go to move a jewel to a square, if we are able to push it, so both front/back or left/right should be free
            left_square_type = self.map.map_layout[x - 1][y]
            right_square_type = self.map.map_layout[x + 1][y]
            left_node = Node((x - 1, y), node)
            right_node = Node((x + 1, y), node)
            if (right_square_type == '.' or right_square_type == 'G' or right_square_type == 'M' or (right_square_type == 'J' and self.node_start == right_node)) and (left_square_type == '.' or left_square_type == 'G' or left_square_type == 'M' or  (left_square_type == 'J' and self.node_start == left_node)):
                nodes.append(Node((x - 1, y), node))
                nodes.append(Node((x + 1, y), node))
            front_square_type = self.map.map_layout[x][y + 1]
            back_square_type = self.map.map_layout[x][y - 1]
            front_node = Node((x, y + 1), node)
            back_node = Node((x, y - 1), node)                  
            if (front_square_type == '.' or front_square_type == 'G' or front_square_type == 'M' or (front_square_type == 'J' and self.node_start == front_node)) and (back_square_type == '.' or back_square_type == 'G' or back_square_type == 'M' or (back_square_type == 'J' and self.node_start == back_node)):
                nodes.append(front_node)
                nodes.append(back_node)
        elif self.search_for_type == 'M':
            points = []
            points.append((x - 1, y))
            points.append((x + 1, y))
            points.append((x, y + 1))
            points.append((x, y - 1))
            for point in points:
                square_type = self.map.map_layout[point[0]][point[1]]
                if square_type == '.' or square_type == 'G':
                    nodes.append(Node(point, node))
        elif self.search_for_type.lower() == 'reverse':            
            points = []
            points.append(((x - 1, y), (x - 2, y)))
            points.append(((x + 1, y), (x + 2, y)))
            points.append(((x, y + 1), (x, y + 2)))
            points.append(((x, y - 1), (x, y - 2)))
            for point in points:
                first_square_type = self.map.map_layout[point[0][0]][point[0][1]]
                second_square_type = self.map.map_layout[point[1][0]][point[1][1]]
                if (first_square_type == '.' or first_square_type == 'G' or (first_square_type == 'J' and point[0][0] == self.node_goal.point[0] and point[0][1] == self.node_goal.point[1])) and (second_square_type == '.' or second_square_type == 'G' or (second_square_type == 'J' and point[1][0] == self.node_goal.point[0] and point[1][1] == self.node_goal.point[1])):
                    nodes.append(Node(point[0], node))
        elif self.search_for_type.lower() == 'obstacle':
            points = []
            points.append((x - 1, y))
            points.append((x + 1, y))
            points.append((x, y + 1))
            points.append((x, y - 1))
            for point in points:
                square_type = self.map.map_layout[point[0]][point[1]]
                if square_type == '.' or square_type == 'G' or square_type == 'J':
                    nodes.append(Node(point, node))
        return nodes
    
    def _score_nodes(self, node_current, surrounding_nodes):
        for node in surrounding_nodes:
            node.cost = self._get_node_cost(node_current, node)
            node.heuristic = self._get_node_heuristic(self.node_goal, node)
            node.score = node.cost + node.heuristic
    
    def _score_compare(self, node_a, node_b):
        if node_a.score > node_b.score:
            return 1
        elif node_a.score == node_b.score:
            return 0
        else:
            return -1
    
    def _construct_path_to_goal(self):
        node = self.node_goal
        while node != self.node_start:
            self.nodes_to_goal.insert(0, node)
            node = node.parent
    
    def set_search_for_type(self, search_for_type):
        self.search_for_type = search_for_type
        
    #@benchmark  
    def do_search(self):
        self.nodes_to_goal = []
        self.open_list = []
        self.closed_list = []
        self.goal_reached = False
        
        open_list_empty = False
        self.open_list.append(self.node_start)
        
        while not (self.goal_reached or open_list_empty):
            self.open_list.sort(cmp = self._score_compare)
            node_current = self.open_list[0]
            self.closed_list.append(node_current)
            self.open_list.remove(node_current)
            surrounding_nodes = self._get_surrounding_nodes(node_current)
            self._score_nodes(node_current, surrounding_nodes)
            
            for node in surrounding_nodes:
                if node in self.open_list:
                    i = self.open_list.index(node)
                    if node.cost < self.open_list[i].cost:
                        self.open_list[i] = node
                else:        
                    if node not in self.closed_list:
                        self.open_list.append(node)
                        if node == self.node_goal:
                            self.node_goal.parent = node.parent
                            self.closed_list.append(node)
                            self._construct_path_to_goal()
                            return True
                        
            if len(self.open_list) == 0:
                #print 'Could not reach goal
                return False
            
class SokoState():
    def __init__(self, soko_map):
        self.jewels = []
        self.goals = []
        self.bricks = []
        self.man = None
        self.map_layout = [['']*soko_map.height for i in xrange(soko_map.width)]
        
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
    
    def __eq__(self, other):
        equal = True
        for jewel in self.jewels:
            if not jewel in other.jewels:
                equal = False
                break
        return equal
    
class SokobanSolver():
    def __init__(self, soko_map):
        self.soko_state = SokoState(soko_map)
        self.searcher = AStarSearch(self.soko_state)
        self.soko_map = soko_map
        self.jewels_final_coordinates = []
         
    def find_path(self, node_start, node_end, search_type):
        self.searcher.set_search_for_type(search_type)
        self.searcher.set_starting_node(node_start)
        self.searcher.set_goal_node(node_end)
        if self.searcher.do_search():
            return self.searcher.nodes_to_goal
        else:
            return None
        
    def detect_obstacle(self, node_start, node_end):
        path = self.find_path(node_start, node_end, 'obstacle')
        if path != None:
            for node in path:
                if node.point in self.soko_state.jewels:
                    return node
        return None
            
    def update_jewel_layout(self, jewel_index, new_point, path = None):
        self.soko_state.map_layout[self.soko_state.jewels[jewel_index][0]][self.soko_state.jewels[jewel_index][1]] = '.'
        self.soko_state.map_layout[new_point[0]][new_point[1]] = 'J'
        self.soko_state.jewels[jewel_index] = new_point
        if path != None:
            for step in path:
                self.soko_map.jewels[jewel_index].x = step.point[0]
                self.soko_map.jewels[jewel_index].y = step.point[1]
                time.sleep(0.3)
        else:
            self.soko_map.jewels[jewel_index].x = new_point[0]
            self.soko_map.jewels[jewel_index].y = new_point[1]
            
    def has_puzzle_been_solved(self):
        done = True
        for jewel in self.soko_state.jewels:
            if not jewel in self.soko_state.goals:
                done = False
        return done
    
    def reversed_puzzle_solved(self):
        for point in self.jewels_final_coordinates:
            if point not in self.soko_state.jewels:
                return False 
        return True
          
    def solve_reverse(self):
        #Move all jewels onto goals, but save original coordinates
        for index, jewel in enumerate(self.soko_state.jewels):
            self.jewels_final_coordinates.append(jewel)
            self.update_jewel_layout(index, self.soko_state.goals[index])
        
        generator_goal_index = itertools.permutations(list(range(len(self.soko_state.goals))), len(self.soko_state.goals))
        generator_jewel_index = itertools.permutations(list(range(len(self.soko_state.jewels))), len(self.soko_state.jewels))
        
        #while not solved:
        for goal_attempt in generator_goal_index:
            print(goal_attempt)
            for jewel_attempt in generator_jewel_index:
                #===============================================================
                # move jewels to goals (Reset map!)
                #===============================================================
                for index in range(len(self.soko_state.jewels)):
                    self.update_jewel_layout(index, self.soko_state.goals[index])
                
                for index in range(len(goal_attempt)):
                    node_goal = Node(self.jewels_final_coordinates[index])
                    node_jewel = Node(self.soko_state.jewels[jewel_attempt[index]])
                    path = self.find_path(node_jewel, node_goal, 'reverse')
                    if path == None:
                        #=======================================================
                        # Try moving an obstacles out of the way!
                        #=======================================================
                        node_obstacle = self.detect_obstacle(node_jewel, node_goal)
                        if node_obstacle != None:
                            print('Obstacle in the way:' + str((node_obstacle.point[0], node_obstacle.point[1])))
                            for i in range(100):
                                #===============================================
                                # find usable place where the obstacle can be 
                                # moved to
                                #===============================================
                                while True:
                                    x = (node_obstacle.point[0] + int(random.random() * 20)) % (self.soko_map.width - 1)
                                    y = (node_obstacle.point[1] + int(random.random() * 20)) % (self.soko_map.height - 1)
                                    node_obstacle_move_to = Node((x, y))
                                    square_type = self.soko_state.map_layout[node_obstacle_move_to.point[0]][node_obstacle_move_to.point[1]]
                                    if square_type == '.' or square_type == 'G':
                                        break
                                    #===========================================
                                    # Try to find a path to move the jewel obstacle
                                    #===========================================
                                    avoid_path = self.find_path(node_obstacle, node_obstacle_move_to, 'reverse')
                                    if avoid_path != None:
                                        #=======================================
                                        # Find index of jewel obstacle, so that
                                        # it can be moved out of the way
                                        #=======================================
                                        obstacle_index = self.jewels_final_coordinates.index(node_obstacle.point)
                                        self.update_jewel_layout(obstacle_index, node_obstacle_move_to.point, avoid_path)
                                        #=======================================
                                        # Now try to place original jewel on goal
                                        #=======================================
                                        path = self.find_path(node_jewel, node_goal, 'reverse')
                                        if path != None:
                                            #===================================
                                            # Now that the obstacle back to original place
                                            #===================================
                                            avoid_path_back = self.find_path(node_obstacle_move_to, node_obstacle, 'reverse')
                                            if avoid_path_back != None:
                                                self.update_jewel_layout(index, self.jewels_final_coordinates[index], path)
                                                self.update_jewel_layout(obstacle_index, node_obstacle.point, avoid_path_back)
                                                break
                        else:
                            break
                    else:
                        self.update_jewel_layout(index, self.jewels_final_coordinates[index], path)
                        
                if self.reversed_puzzle_solved():
                    return True
        return False
    
    def solve(self):
        goal_index = 0
        jewels_goaled = []
        while not self.has_puzzle_been_solved():
            goal_node = Node(self.soko_state.goals[goal_index])
            for jewel_index in xrange(len(self.soko_state.jewels)): 
                if not jewel_index in jewels_goaled:
                    jewel_node = Node(self.soko_state.jewels[jewel_index])
                    jewel_path = self.find_path(jewel_node, goal_node, 'G')
                    if jewel_path != None:
                        print('One found')
                        #Test to see if the man can push the jewel with the currently discovered jewel_path
                        man_start_node = Node(self.soko_state.man)
                        jewel_path_first_step = jewel_path[0]
                        if jewel_path_first_step.point[0] - jewel_node.point[0] == -1:
                            #The jewel is moving left, so the man should position to the right
                            man_end_node = Node((jewel_path_first_step.point[0] + 1, jewel_path_first_step.point[1]))
                        elif jewel_path_first_step.point[0] - jewel_node.point[0] == 1:
                            #The jewel is moving right, so the man should position to the left
                            man_end_node = Node((jewel_path_first_step.point[0] - 1, jewel_path_first_step.point[1]))
                        elif jewel_path_first_step.point[1] - jewel_node.point[1] == -1:
                            #The jewel is moving up, so the man should position at the bottom
                            man_end_node = Node((jewel_path_first_step.point[0], jewel_path_first_step.point[1] + 1))
                        elif jewel_path_first_step.point[1] - jewel_node.point[1] == 1:
                            #The jewel is moving down, so the man should position at the top
                            man_end_node = Node((jewel_path_first_step.point[0], jewel_path_first_step.point[1] - 1))
                        man_path = self.find_path(man_start_node, man_end_node, 'M')
                        if man_path != None:
                            for step in man_path:
                                self.soko_map.man[0].x = step.point[0]
                                self.soko_map.man[0].y = step.point[1]
                                time.sleep(0.1)
                            self.soko_state.man = (self.soko_map.man[0].x, self.soko_map.man[0].y)    
                            self.update_jewel_layout(jewel_index, self.soko_state.goals[goal_index])
                            jewels_goaled.append(jewel_index)
                            for step in jewel_path:
                                self.soko_map.jewels[jewel_index].x = step.point[0]
                                self.soko_map.jewels[jewel_index].y = step.point[1]
                                time.sleep(0.1)                   
                            break
                    else:
                        print('What?')
            #jewels_goaled = []
            goal_index += 1
            goal_index %= len(self.soko_state.goals)
            if goal_index == len(self.soko_state.goals) - 1:
                jewels_goaled = []
        print('Puzzle solved')
        
def main_5():
    pygame.display.set_mode()
    soko_map = Map(get_full_path('/rsc/mymap.txt'))
    solver = SokobanSolver(soko_map)
    tusch = Painter(soko_map)
    tusch.start()    
    print('Going to work')
    solver.solve_reverse()
    
def main_4():
    pygame.display.set_mode()
    soko_map = Map(get_full_path('/rsc/mymap.txt'))
    solver = SokobanSolver(soko_map)

    tusch = Painter(soko_map)
    tusch.start()
    
    solver.solve()    

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
    
    search.set_goal_node(Node(goal))
    search.set_starting_node(Node(start))
    search.do_search()
    
    search.set_goal_node(Node((8,7)))
    search.set_starting_node(Node(goal))
    search.do_search()
    #raw_input()
    
if __name__ == '__main__':
    main_5()