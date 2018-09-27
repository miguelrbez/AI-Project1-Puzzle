import Queue as Q

import time

# import resource

import sys

import math


#### SKELETON CODE ####

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


# Function that Writes to output.txt

### Students need to change the method to have the corresponding parameters

def writeOutput():
    pass

    ### Student Code Goes here


def bfs_search(initial_state, goal_config):

    """BFS search"""
    print 'BFS algorithm working'

    puzzle_config = initial_state.config
    print puzzle_config

    fringe=Frontier()

    fringe.fenqueue(initial_state)

    explored=[]

    while fringe.frontier_list:

        print 1, fringe.frontier_list
        current_state = fringe.fdequeue()

        explored.append(current_state)
        print 2, explored

        if test_goal(current_state, goal_config):
            return 'SUCCESS'

        nodes_to_expand=current_state.expand()
        for state in nodes_to_expand:
            print state.config


    print 3, fringe.frontier_list
    print 4, explored
    print 5, 'BFS algorithm stop'

    return 'FAILURE'

def test_goal(puzzle_state, goal_config):

    """test the state is the goal state or not"""
    if puzzle_state.config==goal_config:
        return [True, puzzle_state]
    else:
        return False
    #Returns False for testing purposes
    #return False


class Board(object):

    def __init__(self, config):
        self.config = config

    def get_board(self):
        boardstr = ''

        for i in self.config:
            boardstr += str(i)

        return boardstr


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


# Main Function that reads in Input and Runs corresponding Algorithm

def main():
    sm = sys.argv[1].lower()

    begin_state = sys.argv[2].split(",")

    begin_state = tuple(map(int, begin_state))

    size = int(math.sqrt(len(begin_state)))

    goal_config = tuple(x for x in range(size**2))

    hard_state = PuzzleState(begin_state, size)

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
    test_list = list(begin_state)
    # print test_list
    # toy = Board(testtuple)
    # print toy.get_board()
    # toy = Board(begin_state)
    # print toy.get_board()
    #test_frontier = Frontier()
    print goal_config


if __name__ == '__main__':
    main()
