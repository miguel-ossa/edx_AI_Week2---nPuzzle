#!/usr/bin/python
import ast  # Abstract Syntax Trees (https://docs.python.org/2/library/ast.html?highlight=ast#module-ast)
from collections import \
    deque  # https://docs.python.org/2/library/collections.html?highlight=collections#module-collections
import time

# Local libraries
import priorityDict
import nodeClass

_DEBUG_LEVEL = 1


def child_node(parent, move):
    x = nodeClass.Node()
    x.depth = parent.depth + 1
    x.parent = parent
    x.move = move
    return x


def new_node(depth, parent):
    x = nodeClass.Node()
    x.depth = depth
    x.parent = parent
    x.move = 0
    return x


class Puzzle:
    def __init__(self, nsize, algorithm, grid):  # , movs=[]):
        """Initialize the n-puzzle problem, with n-size value, tsize the total nodes and initial the goal state from n.
        """

        self.__nsize = nsize
        self.__tsize = pow(self.__nsize, 2)
        self.__goal = range(0, self.__tsize)
        self.__algorithm = algorithm
        self.__grid = grid
        self.__pexpands = {}
        self.__cost_of_path = 0
        self.__final_node = nodeClass.Node()
        self.__start_time = time.time()
        self.__end_time = time.time()
        self.__initial_state = None

        if self.__algorithm == "bfs":
            self.__frontier = deque()
            self.__nodes = deque()  # Queue to show the final path
            self.__moves = [-self.__nsize, self.__nsize, -1, 1]
        elif self.__algorithm == "dfs":
            self.__frontier = deque()
            self.__nodes = deque()  # Queue to show the final path
            self.__moves = [1, -1, self.__nsize, -self.__nsize]
        elif self.__algorithm == "ast" or self.__algorithm == "ida":
            self.__frontier = priorityDict.PriorityDict()
            self.__nodes = dict()  # Queue to show the final path
            self.__moves = [-self.__nsize, self.__nsize, -1, 1]

        for key in range(self.__tsize):
            self.__pexpands[key] = self.getvalues(key)

        self.explored = set()

        self.__nodes_expanded = 0  # the number of nodes that have been expanded
        # self.max_fringe_size = 0 # the maximum size of the frontier set in the lifetime of the algorithm
        self.max_search_depth = 0  # the maximum depth of the search tree in the lifetime of the algorithm

    def printst(self, st):
        """Print the list in a Matrix Format."""

        for (index, value) in enumerate(st):
            print ' %s ' % value,
            if index in [x for x in range(self.__nsize - 1, self.__tsize,
                                          self.__nsize)]:
                print
        print

    """Para cada key (de 0 a nsize) se comprueban los posibles movimientos en sus 
   casillas de partida.

   /-----------\
   | 0 | 1 | 2 |
   |-----------|
   | 3 | 4 | 5 |
   |-----------|
   | 6 | 7 | 8 |
   \-----------/

   Por ejemplo, si sumamos 1 al 0, lo desplazamos a la casilla 1. Si le sumamos 3, 
   ira a parar a la casilla de abajo: la 3.  
   1  - RIGHT
   3  - DOWN
   -1 - LEFT
   -3 - UP
    """

    def getvalues(self, key):
        valid = []
        for x in self.__moves:
            if 0 <= key + x < self.__tsize:  # up, down
                # [2, 5, 8] right
                if x == 1 and key in range(self.__nsize - 1, self.__tsize,
                                           self.__nsize):
                    continue
                # [0, 3, 6] left
                if x == -1 and key in range(0, self.__tsize, self.__nsize):
                    continue
                valid.append(x)
        return tuple(valid)

    def neighbors(self, st):

        pos = st.index(0)

        # check possible moves at this position
        moves = self.__pexpands[pos]
        expstates = []
        for mv in moves:
            nstate = st[:]
            (nstate[pos + mv], nstate[pos]) = (nstate[pos], nstate[pos + mv])
            expstates.append(nstate)
        return zip(expstates, moves)

    def manhattan_distance(self, st, target):
        mdist = 0
        for node in st:
            if node != 0:
                gdist = abs(target.index(node) - st.index(node))
                (jumps, steps) = (gdist // self.__nsize, gdist % self.__nsize)
                mdist += jumps + steps
        return mdist

    def uninformed_search_bfs(self, initial_state):
        self.__initial_state = initial_state
        self.__frontier.append(str(initial_state))
        node = new_node(0, None)
        self.__nodes.append(node)  # Collect nodes for statistics
        # self.max_fringe_size = 1
        while self.__frontier:
            state = ast.literal_eval(self.__frontier.popleft())
            self.explored.add(tuple(state))
            node = self.__nodes.popleft()
            if state == self.__goal:
                return node
            self.__nodes_expanded += 1  # Statistics
            for neighbor, move in self.neighbors(state):
                if not tuple(neighbor) in self.explored and not str(neighbor) in self.__frontier:
                    self.__frontier.append(str(neighbor))
                    self.__nodes.append(child_node(node, move))
                    if node.depth + 1 > self.max_search_depth:
                        self.max_search_depth = node.depth + 1  # Statistics
        return

    def uninformed_search_dfs(self, initial_state):
        self.__initial_state = initial_state
        self.__frontier.append(str(initial_state))
        node = new_node(0, None)
        self.__nodes.append(node)
        # self.max_fringe_size = 1
        while self.__frontier:
            state = ast.literal_eval(self.__frontier.pop())
            self.explored.add(tuple(state))
            node = self.__nodes.pop()
            if state == self.__goal:
                return node
            self.__nodes_expanded += 1
            for neighbor, move in self.neighbors(state):
                if not tuple(neighbor) in self.explored and not str(neighbor) in self.__frontier:
                    self.__frontier.append(str(neighbor))
                    self.__nodes.append(child_node(node, move))
                    if node.depth + 1 > self.max_search_depth:
                        self.max_search_depth = node.depth + 1
        return

    def ast_search(self, initial_state):
        self.__initial_state = initial_state
        self.__frontier[tuple(initial_state)] = 0
        node = new_node(0, None)
        node.heuristic = 0
        self.__nodes[tuple(initial_state)] = node
        # self.max_fringe_size = 1
        while self.__frontier:
            state = list(self.__frontier.pop_smallest())
            self.explored.add(tuple(state))
            node = self.__nodes[tuple(state)]
            if state == self.__goal:
                return node
            self.__nodes_expanded += 1
            for neighbor, move in self.neighbors(state):
                if not tuple(neighbor) in self.explored:
                    child = child_node(node, move)
                    depth = child.depth
                    if not tuple(neighbor) in self.__frontier:
                        self.__frontier[tuple(neighbor)] = child.depth
                        self.__nodes[tuple(neighbor)] = child
                        if child.depth > self.max_search_depth:
                            self.max_search_depth = child.depth
                    else:
                        if self.__frontier[tuple(neighbor)] > depth:
                            self.__frontier[tuple(neighbor)] = depth
        return

    def ida_search(self, initial_state):
        self.__initial_state = initial_state
        self.__frontier[tuple(initial_state)] = 0
        node = new_node(0, None)
        node.heuristic = 0
        self.__nodes[tuple(initial_state)] = node
        # self.max_fringe_size = 1
        while self.__frontier:
            state = list(self.__frontier.pop_smallest())
            self.explored.add(tuple(state))
            node = self.__nodes[tuple(state)]
            if state == self.__goal:
                return node
            self.__nodes_expanded += 1
            for neighbor, move in self.neighbors(state):
                if not tuple(neighbor) in self.explored:
                    child = child_node(node, move)
                    child.heuristic = node.heuristic + self.manhattan_distance(state, neighbor)  # g(n)
                    dist = child.heuristic + self.manhattan_distance(neighbor, self.__goal)  # h(n)
                    if not tuple(neighbor) in self.__frontier:
                        self.__frontier[tuple(neighbor)] = dist
                        self.__nodes[tuple(neighbor)] = child
                        if child.depth > self.max_search_depth:
                            self.max_search_depth = child.depth
                    else:
                        if self.__frontier[tuple(neighbor)] > dist:
                            self.__frontier[tuple(neighbor)] = dist
        return

    def build_moves(self):
        moves = deque()
        moves.append(self.__final_node.move)
        current = self.__final_node.parent
        while current:
            self.__cost_of_path += 1
            if current.parent is not None:
                moves.append(current.move)
            current = current.parent
        return moves

    def build_list_of_moves(self, moves):
        initial_state = self.__initial_state
        lst_moves = []
        self.__grid.printGrid(initial_state)
        state = initial_state
        while moves:
            mv = moves.pop()
            state = self.__grid.makeMove(state, mv)
            self.__grid.printGrid(state)
            lst_moves.append(self.__grid.getMove(mv))

        return lst_moves

    def build_output(self, lst_moves):
        f = open('output.txt', 'w')
        f.write("path_to_goal: " + str(lst_moves) + "\n")
        f.write("cost_of_path: " + str(self.__cost_of_path) + "\n")
        f.write("nodes_expanded: " + str(self.__nodes_expanded) + "\n")
        f.write("search_depth: " + str(self.__final_node.depth) + "\n")
        f.write("max_search_depth: " + str(self.max_search_depth) + "\n")
        f.write(("running_time: %s" % (self.__end_time - self.__start_time)) + "\n")
        f.close()

        if _DEBUG_LEVEL > 0:
            f = open('output.txt', 'r')
            for line in f:
                print line,
            f.close()
        return

    def build_results(self):
        moves = self.build_moves()
        lst_moves = self.build_list_of_moves(moves)
        self.build_output(lst_moves)
        return

    def execute_algorithm(self, start_position):
        if self.__algorithm == "bfs":
            self.__final_node = self.uninformed_search_bfs(start_position)
        elif self.__algorithm == "dfs":
            self.__final_node = self.uninformed_search_dfs(start_position)
        elif self.__algorithm == "ast":
            self.__final_node = self.ast_search(start_position)
        elif self.__algorithm == "ida":
            self.__final_node = self.ida_search(start_position)
        return

    def solve_it(self, start_position):
        self.__start_time = time.time()
        self.execute_algorithm(start_position)
        self.__end_time = time.time()

        # rusage_denom = 1024.
        # if sys.platform == 'darwin':
        # rusage_denom = rusage_denom * rusage_denom
        # mem = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss / rusage_denom / 100

        return


"""

C:\Python27\python.exe "D:/Development/AI-Columbia-Exercises-master/edx_AI_Week2 - nPuzzle/driver.py" ida 0,8,7,6,5,4,3,2,1
path_to_goal: ['Right', 'Down', 'Down', 'Right', 'Up', 'Up', 'Left', 'Down', 'Down', 'Left', 'Up', 'Right', 'Down', 'Right', 'Up', 'Up', 'Left', 'Left', 'Down', 'Right', 'Up', 'Right', 'Down', 'Left', 'Down', 'Right', 'Up', 'Up', 'Left', 'Left']
cost_of_path: 30
nodes_expanded: 9859
search_depth: 30
max_search_depth: 30
running_time: 0.430999994278

C:\Python27\python.exe "D:/Development/AI-Columbia-Exercises-master/edx_AI_Week2 - nPuzzle/driver.py" ast 0,8,7,6,5,4,3,2,1
path_to_goal: ['Down', 'Right', 'Down', 'Right', 'Up', 'Up', 'Left', 'Down', 'Left', 'Up', 'Right', 'Down', 'Down', 'Left', 'Up', 'Right', 'Down', 'Right', 'Up', 'Up', 'Left', 'Left', 'Down', 'Right', 'Down', 'Right', 'Up', 'Up', 'Left', 'Left']
cost_of_path: 30
nodes_expanded: 181217
search_depth: 30
max_search_depth: 30
running_time: 3.91900014877

C:\Python27\python.exe "D:/Development/AI-Columbia-Exercises-master/edx_AI_Week2 - nPuzzle/driver.py" bfs 0,1,7,6,3,4,5,2,8
path_to_goal: ['Right', 'Right', 'Down', 'Down', 'Left', 'Left', 'Up', 'Right', 'Right', 'Down', 'Left', 'Up', 'Up', 'Right', 'Down', 'Down', 'Left', 'Up', 'Up', 'Left']
cost_of_path: 20
nodes_expanded: 53341
search_depth: 20
max_search_depth: 21
running_time: 32.757999897

C:\Python27\python.exe -m driver dfs 0,8,7,6,5,4,3,2,1
path_to_goal: HORRIBLE
cost_of_path: 41910
nodes_expanded: 144633
search_depth: 41910
max_search_depth: 65982
running_time: 101.28099989
"""
