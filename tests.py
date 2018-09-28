import sys
import psutil
print("psutil", psutil.Process().memory_info().rss)

test_str = 'path_to_goal: '
test_str += 'Up'

str_list=[]
str_list.append(test_str)
str_list.append('Javier')
with open('test.txt', 'w') as test_file:
    test_file.writelines(str_list)