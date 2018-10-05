import sys
import psutil
# print("psutil", psutil.Process().memory_info().rss)
#
# test_str = 'path_to_goal: '
# test_str += 'Up'
#
# str_list=[]
# str_list.extend([test_str, 'dsgdfg', str(3),'\n'])
# kk=[test_str, 'dsgdfg', str(3),'\n']
# for i in kk:
#     str_list.append(str(i))
# str_list.append('\n')
# str_list.append('Javier')
# with open('test.txt', 'w') as test_file:
#     test_file.writelines(str_list)

def calculate_manhattan_dist(idx, value, n):
    """calculate the manhattan distance of a tile"""

    # Calculate current tile position
    current_row = idx / n
    current_col = idx % n

    # Calculate goal tile position
    goal_row = value / n
    goal_col = value % n

    manhattan_dist = abs(goal_row - current_row) + abs(goal_col - current_col)

    return abs(manhattan_dist)

def calculate_total_cost(state):
    """calculate the total estimated cost of a state"""

    h_total_cost = 0

    for i, item in enumerate(config):

        if item != 0:
            h_total_cost += calculate_manhattan_dist(i, item, 3)

    return h_total_cost

config = (1,2,5,3,4,0,6,7,8)

print 'Total cost: ', calculate_total_cost(config)

hhh = sorted(list(config))
print hhh
for i in hhh:
    print i
    if 4 < i:
        hhh.insert(i,88)
        break
print hhh