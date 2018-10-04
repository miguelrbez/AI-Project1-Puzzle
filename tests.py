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

print calculate_manhattan_dist(4,2,3)