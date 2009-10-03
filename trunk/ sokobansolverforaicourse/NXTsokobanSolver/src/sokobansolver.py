'''
Created on Oct 2, 2009

@author: zagnut
'''
import os
import copy

class MapRepresantation():
    def __init__(self):
        self.jewel = 'J'
        self.empty = '.'
        self.wall = 'X'
        self.goal = 'G'
        self.man = 'M'
        
class SokobanState():
    def __init__(self, map_rep, parent):
        self.map_rep = map_rep
        self.map_layout = None
        self.map_jewels = []
        self.map_man = []
        self.map_goals = []
        self.parent = None
        self.cost = float('inf')
    
    def __eq__(self, other):
        if other == None:
            return False
        for jewel in self.map_jewels:
            if jewel not in other.map_jewels:
                return False
        if self.map_man != other.map_man:
            return False
        return True
    
    def get_copy(self):
        return copy.deepcopy(self)
    
    def update_jewel(self, jewel, new_coordinates):
        self.map_layout[jewel[0]][jewel[1]] = self.map_rep.empty
        self.map_layout[new_coordinates[0]][new_coordinates[1]] = self.map_rep.jewel
        index = self.map_jewels.index(jewel)
        self.map_jewels[index] = new_coordinates
        
    def update_man(self, new_coordinates):
        self.map_layout[self.map_man[0]][self.map_man[1]] = self.map_rep.empty
        self.map_layout[new_coordinates[0]][new_coordinates[1]] = self.map_rep.man
        self.map_man = new_coordinates
        
class MapParser():
    def __init__(self, map_path, map_rep):
        self.map_path = self._get_full_path(map_path)
        self.map_rep = map_rep
        
    def _get_full_path(self, relative_path):
        return os.path.dirname(os.path.dirname(os.path.abspath( __file__ ))) + relative_path
    
    def _get_map_layout_from_text(self):
        map_text = [t.replace('\n', '') for t in open(self.map_path) if t.count('X') > 0]
        
        #Determine maximum length of a line, so that we can create a square map array!
        maximum_length = 0 
        for line in map_text:
            maximum_length = max(maximum_length, len(line))
            
        #Create the map array from the text file. Notice the 'x y' reversal
        map_layout = [[''] * len(map_text) for i in range(maximum_length)]
        for index_line, line in enumerate(map_text):
            for index_char in range(maximum_length):
                if index_char < len(line):
                    map_layout[index_char][index_line] = map_text[index_line][index_char]
                else:
                    map_layout[index_char][index_line] = ''
        
        return map_layout
    
    def create_initial_sokoban_state(self):        
        map_layout = self._get_map_layout_from_text()
        man = []
        goals = []
        jewels = []
        
        #Get the position of the man, jewels and goals
        for x in range(len(map_layout)):
            for y in range(len(map_layout[0])):
                if map_layout[x][y] == self.map_rep.jewel:
                    jewels.append([x, y])
                elif map_layout[x][y] == self.map_rep.goal:
                    goals.append([x, y])
                elif map_layout[x][y] == self.map_rep.man:
                    man = [x, y]                
        
        #Now we have the information we need to create the initial state
        initial_state = SokobanState(self.map_rep, None)
        initial_state.map_goals = goals
        initial_state.map_jewels = jewels
        initial_state.map_layout = map_layout
        initial_state.map_man = man
        return initial_state

class AStarSearcher():
    def __init__(self):
        self.fringe = []
        self.closed_states = []
        self.state_goal = None
        self.state_initial = None
        self.path_to_goal = []
        self.run_counter = 0
        
    def evaluate_state(self, state):
        raise NotImplementedError
    
    def expand_fringe(self, state):
        raise NotImplementedError
    
    def is_state_valid(self, state):
        raise NotImplementedError
    
    def is_goal_state(self, state):
        raise NotImplementedError
    
    def get_cost(self, state):
        return state.cost
    
    def search(self):
        self.fringe = []
        self.closed_states = []
        self.path_to_goal = []
        self.fringe.append(self.state_initial)
        while len(self.fringe) > 0:
            self.fringe.sort(key = self.get_cost)
            state_current = self.fringe.pop(0)
            self.closed_states.append(state_current)
            if self.is_goal_state(state_current):
                #Construct path to goal
                state_step = state_current
                while state_step != self.state_initial:
                    self.path_to_goal.append(state_step)
                    state_step = state_step.parent
                return True
            fringe_new = self.expand_fringe(state_current)
            for state in fringe_new:
                if self.is_state_valid(state):
                    self.evaluate_state(state)
                    if state in self.fringe:
                        index = self.fringe.index(state)
                        if state.cost < self.fringe[index].cost:
                            self.fringe[index] = state
                    else:
                        if state not in self.closed_states:
                            self.fringe.append(state)
        return False
    
class ManPathFinder(AStarSearcher):
    def __init__(self):
        super(ManPathFinder, self).__init__()
        
    def is_goal_state(self, state):
        if state.map_man == self.state_goal.map_man:
            return True
        return False
    
    def expand_fringe(self, state):
        fringe = []     
        nodes = []
        nodes.append([state.map_man[0] - 1, state.map_man[1]])
        nodes.append([state.map_man[0] + 1, state.map_man[1]])
        nodes.append([state.map_man[0], state.map_man[1] - 1])
        nodes.append([state.map_man[0], state.map_man[1] + 1])
        
        for node in nodes:
            square_type = state.map_layout[node[0]][node[1]]
            if square_type == state.map_rep.empty or square_type == state.map_rep.goal:
                new_state = state.get_copy()
                new_state.parent = state
                new_state.map_man = node
                fringe.append(new_state)
        return fringe
    
    def evaluate_state(self, state):
        state.cost = abs(state.map_man[0] - self.state_goal.map_man[0]) + abs(state.map_man[1] - self.state_goal.map_man[1]) + 1
    
    def is_state_valid(self, state):
        return True
    

class SokobanSolver(AStarSearcher):
    def __init__(self):
        super(SokobanSolver, self).__init__()
        self.man_path_finder = ManPathFinder()
        self.state_soko_init = MapParser('/rsc/map2.txt', map_rep).create_initial_sokoban_state()
    
    def is_goal_state(self, state):
        for jewel in state.map_jewels:
            if jewel not in state.map_goals:
                return False
        return True
    
    def evaluate_state(self, state):
        heurist = 0
        #First get the heuristc
        for jewel in state.map_jewels:
            if jewel in state.map_goals:
                continue
            minimum_dist = float('inf')
            for goal in state.map_goals:
                dist = abs(goal[0] - jewel[0]) + abs(goal[1] - jewel[1])
                if dist < minimum_dist:
                    minimum_dist = dist 
            if minimum_dist < float('inf'):
                heurist += minimum_dist
            else:
                heurist += 10000
        
        #Now get the cost
        score = len(self.man_path_finder.path_to_goal)
        return score + heurist
        
    def expand_fringe(self, state):
        self.run_counter += 1
        #print(isinstance(self, SokobanSolver))
        print(self.run_counter)
        fringe = []
        for jewel in state.map_jewels:
            
            #Test up
            new_state = self.get_new_jewel_position(state, jewel, 'UP')
            if new_state != None:
                fringe.append(new_state)
            #Test down
            new_state = self.get_new_jewel_position(state, jewel, 'DOWN')
            if new_state != None:
                fringe.append(new_state)
            #Test left
            new_state = self.get_new_jewel_position(state, jewel, 'LEFT')
            if new_state != None:
                fringe.append(new_state)
            #Test right
            new_state = self.get_new_jewel_position(state, jewel, 'RIGHT')
            if new_state != None:
                fringe.append(new_state)
        return fringe
                
    def get_new_jewel_position(self, state, jewel, direction):
        if direction == 'UP':
            new_jewel_coordinate = [jewel[0], jewel[1] - 1]
            new_man_coordinate = [jewel[0], jewel[1] + 1]
        elif direction == 'DOWN':
            new_jewel_coordinate = [jewel[0], jewel[1] + 1]
            new_man_coordinate = [jewel[0], jewel[1] - 1]  
        elif direction == 'LEFT':
            new_jewel_coordinate = [jewel[0] - 1, jewel[1]]
            new_man_coordinate = [jewel[0] + 1, jewel[1]]  
        elif direction == 'RIGHT':
            new_jewel_coordinate = [jewel[0] + 1, jewel[1]]
            new_man_coordinate = [jewel[0] - 1, jewel[1]]
        
        square_type = state.map_layout[new_jewel_coordinate[0]][new_jewel_coordinate[1]]
        if square_type == state.map_rep.empty or square_type == state.map_rep.goal:
                #Test if the state would be valid
                new_state = state.get_copy()
                #Test if the man can get to the correct spot
                new_state.update_man(new_man_coordinate)
                self.man_path_finder.state_goal = new_state
                self.man_path_finder.state_initial = state
                if self.man_path_finder.search():
                    #Move the man and the jewel
                    new_state.update_man(jewel)
                    new_state.update_jewel(jewel, new_jewel_coordinate)
                    new_state.parent = state
                    return new_state
        return None
    
    def is_state_valid(self, state):
        for jewel in state.map_jewels:
            if jewel in state.map_goals:
                continue
            
            up_square = state.map_layout[jewel[0]][jewel[1] - 1]
            down_square = state.map_layout[jewel[0]][jewel[1] + 1]
            left_square = state.map_layout[jewel[0] - 1][jewel[1]]
            right_square = state.map_layout[jewel[0] + 1][jewel[1]]
            
            if up_square == state.map_rep.wall or down_square == state.map_rep.wall:
                if left_square == state.map_rep.wall or right_square == state.map_rep.wall:
                    return False
            
            if jewel[0] == 1:
                return False
            if jewel[1] == 1 and jewel[0] > 4:
                return False
            if jewel[1] == 5 and jewel[0] > 3:
                return False
            
        return True
    
if __name__ == '__main__':
    map_rep = MapRepresantation()
    parser = MapParser('/rsc/map2.txt', map_rep)
    state_soko_init = parser.create_initial_sokoban_state()
    solver = SokobanSolver()
    solver.state_initial = state_soko_init
    if solver.search():
        print('Found solution')
    else:
        print('Could not find solution') 