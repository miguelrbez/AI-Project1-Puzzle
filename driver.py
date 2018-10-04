import Queue as Q

import time

# import resource

import sys

import math

import psutil

## The Class that Represents the Puzzle
class PuzzleState(object):
    """docstring for PuzzleState"""

    def __init__(self, config, n, parent=None, action="Initial", cost=0):

        if n * n != len(config) or n < 2:
            raise Exception("the length of config is not correct!")

        self.n = n

        self.cost = cost

        self.parent = parent

        self.action = action

        self.dimension = n

        self.config = config

        self.h_cost = self.calculate_h_cost()

        self.children = []

        for i, item in enumerate(self.config):

            if item == 0:
                self.blank_row = i / self.n

                self.blank_col = i % self.n

                break

    def calculate_h_cost(self):

        """calculate the total estimated cost of a state"""

        h_cost = 0

        for i, item in enumerate(self.config):

            if item != 0:
                h_cost += calculate_manhattan_dist(i, item, self.n)

        return h_cost

    def display(self):

        for i in range(self.n):

            line = []

            offset = i * self.n

            for j in range(self.n):
                line.append(self.config[offset + j])

            print line

    def move_left(self):

        if self.blank_col == 0:

            return None

        else:

            blank_index = self.blank_row * self.n + self.blank_col

            target = blank_index - 1

            new_config = list(self.config)

            new_config[blank_index], new_config[target] = new_config[target], new_config[blank_index]

            return PuzzleState(tuple(new_config), self.n, parent=self, action="Left", cost=self.cost + 1)

    def move_right(self):

        if self.blank_col == self.n - 1:

            return None

        else:

            blank_index = self.blank_row * self.n + self.blank_col

            target = blank_index + 1

            new_config = list(self.config)

            new_config[blank_index], new_config[target] = new_config[target], new_config[blank_index]

            return PuzzleState(tuple(new_config), self.n, parent=self, action="Right", cost=self.cost + 1)

    def move_up(self):

        if self.blank_row == 0:

            return None

        else:

            blank_index = self.blank_row * self.n + self.blank_col

            target = blank_index - self.n

            new_config = list(self.config)

            new_config[blank_index], new_config[target] = new_config[target], new_config[blank_index]

            return PuzzleState(tuple(new_config), self.n, parent=self, action="Up", cost=self.cost + 1)

    def move_down(self):

        if self.blank_row == self.n - 1:

            return None

        else:

            blank_index = self.blank_row * self.n + self.blank_col

            target = blank_index + self.n

            new_config = list(self.config)

            new_config[blank_index], new_config[target] = new_config[target], new_config[blank_index]

            return PuzzleState(tuple(new_config), self.n, parent=self, action="Down", cost=self.cost + 1)

    def expand(self):

        """expand the node"""

        # add child nodes in order of UDLR

        if len(self.children) == 0:

            up_child = self.move_up()

            if up_child is not None:
                self.children.append(up_child)

            down_child = self.move_down()

            if down_child is not None:
                self.children.append(down_child)

            left_child = self.move_left()

            if left_child is not None:
                self.children.append(left_child)

            right_child = self.move_right()

            if right_child is not None:
                self.children.append(right_child)

        return self.children


class Board(object):

    def __init__(self, config):

        self.config = config

    def get_board(self):

        config_str = ''

        for tile in self.config:
            config_str += str(tile)

        config_int = int(config_str)

        return config_int


# noinspection SpellCheckingInspection
class Frontier(object):

    def __init__(self):

        self.frontier_list = []

    def fenqueue(self, i):

        self.frontier_list.append(i)

    def fdequeue(self):

        i = self.frontier_list[0]

        self.frontier_list = self.frontier_list[1:]

        return i

    def fpush(self, i):

        self.frontier_list.append(i)

    def fpop(self):

        i = self.frontier_list[-1]

        self.frontier_list.pop(-1)

        return i


# Function that Writes to output.txt
def writeOutput(str_list):

    with open('output.txt', 'w') as output_file:

        output_file.writelines(str_list)

def get_path_to_goal(goal_state, explored):

    path_to_goal = []

    output_str_path_and_cost = []

    current_state_path = goal_state

    explored_set_path = explored

    while current_state_path.parent != None:

        path_to_goal.insert(0, current_state_path.action)

        current_state_path = current_state_path.parent

    return path_to_goal

def bfs_search(initial_state, goal_config):

    """BFS search"""
    print 'BFS algorithm working'

    # Initialize output string list
    output_str_list = []

    fringe=Frontier()

    fringe.fenqueue(initial_state)

    explored = set()

    # Initialize Fringe/Explored config list
    fringe_explored_config_set = set()

    nodes_expanded = 0

    max_search_depth = initial_state.cost

    # Count to limit number of nodes to explore
    explored_nodes_count = -1

    while fringe.frontier_list:

        explored_nodes_count += 1

        if explored_nodes_count%5000==0:
            print 'count ', explored_nodes_count
            print psutil.Process().memory_info().rss

        # Dequeue state from Fringe
        current_state = fringe.fdequeue()

        # Append exploring state to Explored
        explored.add(current_state)

        # # Append current state config to Fringe/Explored config list
        # fringe_explored_config_set.append(str(current_state.config))

        # Append current state string config to Fringe/Explored config list
        board_config = Board(current_state.config)
        fringe_explored_config_set.add(board_config.get_board())

        # Check solution
        if test_goal(current_state, goal_config):

            # # Print Fringe
            #             # for i, state in enumerate(fringe.frontier_list):
            #             #     print 'Fringe: ', i + 1, state.config
            #             #
            #             # # Print Explored
            #             # for i, state in enumerate(explored):
            #             #     print 'Explored: ', i + 1, state.config

            print 'Final count: ', explored_nodes_count
            print 'BFS algorithm stop'

            path_to_goal = get_path_to_goal(current_state, explored)
            output_str_list.extend(['path_to_goal: ', str(path_to_goal), '\n', 'cost_of_path: ', str(len(path_to_goal)), '\n'])
            output_str_list.extend(['nodes_expanded: ', str(explored_nodes_count), '\n'])
            output_str_list.extend(['search_depth: ', str(len(path_to_goal)), '\n'])
            output_str_list.extend(['max_search_depth: ', str(max_search_depth)])

            print max_search_depth

            return output_str_list

        # Expand nodes and add them to Fringe if not there neither in Explored already
        nodes_to_expand=current_state.expand()

        for expanded_node in nodes_to_expand:

            # Create board config of expanded node
            expanded_board = Board(expanded_node.config)

            #if str(expanded_node.config) not in fringe_explored_config_set:
            if expanded_board.get_board() not in fringe_explored_config_set:

                fringe.fenqueue(expanded_node)

                #fringe_explored_config_set.append(str(expanded_node.config))
                fringe_explored_config_set.add(expanded_board.get_board())

                nodes_expanded += 1

                # Check if it is the deepest node
                if expanded_node.cost > max_search_depth:
                    max_search_depth = expanded_node.cost

    # # Print Fringe
    # for i, state in enumerate(fringe.frontier_list):
    #     print 'Fringe: ', i+1, state.config
    #
    # # Print Explored
    # for i, state in enumerate(explored):
    #     print 'Explored: ', i+1, state.config

    print 'BFS algorithm stop'

    return 'FAILURE'

def dfs_search(initial_state, goal_config):

    """DFS search"""

    print 'DFS algorithm working'

    # Initialize output string list
    output_str_list = []

    fringe = Frontier()

    fringe.fpush(initial_state)

    explored = set()

    # Initialize Fringe/Explored config list
    fringe_explored_config_set = set()

    nodes_expanded = 0

    max_search_depth = initial_state.cost

    # Count to limit number of nodes to explore
    explored_nodes_count = -1

    while fringe.frontier_list:

        explored_nodes_count += 1

        if explored_nodes_count % 5000 == 0:
            print 'count ', explored_nodes_count
            print psutil.Process().memory_info().rss

        # Pop state from Fringe
        current_state = fringe.fpop()

        # Append exploring state to Explored
        explored.add(current_state)

        # Append current state string config to Fringe/Explored config list
        board_config = Board(current_state.config)
        fringe_explored_config_set.add(board_config.get_board())

        # Check solution
        if test_goal(current_state, goal_config):
            # # Print Fringe
            #             # for i, state in enumerate(fringe.frontier_list):
            #             #     print 'Fringe: ', i + 1, state.config
            #             #
            #             # # Print Explored
            #             # for i, state in enumerate(explored):
            #             #     print 'Explored: ', i + 1, state.config

            print 'Final count: ', explored_nodes_count
            print 'DFS algorithm stop'

            path_to_goal = get_path_to_goal(current_state, explored)
            output_str_list.extend(
                ['path_to_goal: ', str(path_to_goal), '\n', 'cost_of_path: ', str(len(path_to_goal)), '\n'])
            output_str_list.extend(['nodes_expanded: ', str(explored_nodes_count), '\n'])
            output_str_list.extend(['search_depth: ', str(len(path_to_goal)), '\n'])
            output_str_list.extend(['max_search_depth: ', str(max_search_depth)])

            print max_search_depth

            return output_str_list

        # Expand nodes and add them to Fringe if not there neither in Explored already
        nodes_to_expand = current_state.expand()
        nodes_to_expand = nodes_to_expand[::-1]

        for expanded_node in nodes_to_expand:

            # Create board config of expanded node
            expanded_board = Board(expanded_node.config)

            # if str(expanded_node.config) not in fringe_explored_config_set:
            if expanded_board.get_board() not in fringe_explored_config_set:

                fringe.fpush(expanded_node)

                # fringe_explored_config_set.append(str(expanded_node.config))
                fringe_explored_config_set.add(expanded_board.get_board())

                nodes_expanded += 1

                # Check if it is the deepest node
                if expanded_node.cost > max_search_depth:
                    max_search_depth = expanded_node.cost

    # # Print Fringe
    # for i, state in enumerate(fringe.frontier_list):
    #     print 'Fringe: ', i+1, state.config
    #
    # # Print Explored
    # for i, state in enumerate(explored):
    #     print 'Explored: ', i+1, state.config

    print 'BFS algorithm stop'

    return 'FAILURE'

def A_star_search(initial_state):

    """A * search"""
    print 'A* algorithm working'

    # Initialize output string list
    output_str_list = []

    size = initial_state.n

    goal_config = tuple(x for x in range(size ** 2))

    return initial_state.calculate_h_cost()

def calculate_total_cost(state):

    """calculate the total estimated cost of a state"""

    return state.cost + state.h_cost

# calculate the manhattan distance of a tile

def calculate_manhattan_dist(idx, value, n):

    # Calculate current tile position
    current_row = idx / n
    current_col = idx % n

    # Calculate goal tile position
    goal_row = value / n
    goal_col = value % n

    manhattan_dist = abs(goal_row - current_row) + abs(goal_col - current_col)

    return abs(manhattan_dist)

def test_goal(puzzle_state, goal_config):

    """test the state is the goal state or not"""

    if puzzle_state.config==goal_config:

        return [True, puzzle_state]

    else:

        return False

# Main Function that reads in Input and Runs corresponding Algorithm

def main():
    sm = sys.argv[1].lower()

    begin_state = sys.argv[2].split(",")

    begin_state = tuple(map(int, begin_state))

    size = int(math.sqrt(len(begin_state)))

    goal_config = tuple(x for x in range(size**2))

    hard_state = PuzzleState(begin_state, size)

    # String list to be written in 'output.txt'
    str_list = []

    if sm == "bfs":

        #print bfs_search(hard_state, goal_config)
        writeOutput(bfs_search(hard_state, goal_config))

    elif sm == "dfs":

        writeOutput(dfs_search(hard_state, goal_config))

    elif sm == "ast":

        print A_star_search(hard_state)

    else:

        print("Enter valid command arguments !")

if __name__ == '__main__':
    main()
    print psutil.Process().memory_info().rss
