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

        self.children = []

        for i, item in enumerate(self.config):

            if item == 0:
                self.blank_row = i / self.n

                self.blank_col = i % self.n

                break

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
        self.frontier_config_list=[]

    def fenqueue(self, i):

        self.frontier_list.append(i)

    def fdequeue(self):

        i = self.frontier_list[0]

        self.frontier_list = self.frontier_list[1:]

        return i


# Function that Writes to output.txt
def writeOutput(str_list):

    with open('output.txt', 'w') as output_file:

        output_file.writelines(str_list)

def bfs_search(initial_state, goal_config):

    """BFS search"""
    print 'BFS algorithm working'

    fringe=Frontier()

    fringe.fenqueue(initial_state)

    explored=[]

    # Initialize Fringe/Explored config list
    fringe_explored_config_set = set()

    # Count to limit number of nodes to explore
    count = 0

    while fringe.frontier_list and count<55000:

        count += 1

        if count%5000==0:
            print 'count ', count
            print psutil.Process().memory_info().rss

        # Dequeue state from Fringe
        current_state = fringe.fdequeue()

        # Append exploring state to Explored
        explored.append(current_state)

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

            print 'Final count: ', count
            print 'BFS algorithm stop'

            return 'SUCCESS'

        # Expand nodes and add them to Fringe if not there neither in Explored already
        nodes_to_expand=current_state.expand()

        for expanded_node in nodes_to_expand:
            # Print Expanded
            #print 'Expanded: ', expanded_node.config

            # Create board config of expanded node
            expanded_board = Board(expanded_node.config)

            #if str(expanded_node.config) not in fringe_explored_config_set:
            if expanded_board.get_board() not in fringe_explored_config_set:

                fringe.fenqueue(expanded_node)

                #fringe_explored_config_set.append(str(expanded_node.config))
                fringe_explored_config_set.add(expanded_board.get_board())

    # # Print Fringe
    # for i, state in enumerate(fringe.frontier_list):
    #     print 'Fringe: ', i+1, state.config
    #
    # # Print Explored
    # for i, state in enumerate(explored):
    #     print 'Explored: ', i+1, state.config

    print 'BFS algorithm stop'

    return 'FAILURE'

def test_goal(puzzle_state, goal_config):

    """test the state is the goal state or not"""

    if puzzle_state.config==goal_config:

        return [True, puzzle_state]

    else:

        return False

    #Returns False for testing purposes
    #return False

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

        print bfs_search(hard_state, goal_config)

    elif sm == "dfs":

        dfs_search(hard_state)

    elif sm == "ast":

        A_star_search(hard_state)

    else:

        print("Enter valid command arguments !")

    '''Tests'''
    # testtuple = 0, 8, 7, 6, 5, 4, 3, 2, 1
    #test_list = list(begin_state)
    # print test_list
    # toy = Board(testtuple)
    # print toy.get_board()
    # toy = Board(begin_state)
    # print toy.get_board()
    # test_frontier = Frontier()
    # test_frontier.fenqueue(hard_state)

    # Memory usage
    for i in ['final', ',', psutil.Process().memory_info().rss, '\n']:
        str_list.append(str(i))

    writeOutput(str_list)

if __name__ == '__main__':
    main()
    print psutil.Process().memory_info().rss
