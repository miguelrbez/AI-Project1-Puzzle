import sys
import psutil
# print("psutil", psutil.Process().memory_info().rss)
#
test_str = 'path_to_goal: '
test_str += 'Up'

str_list=[]
str_list.extend([test_str, 'dsgdfg', str(3),'\n'])
kk=[test_str, 'dsgdfg', str(3),'\n']
for i in kk:
    str_list.append(str(i))
str_list.append('\n')
str_list.append('Javier')
with open('test.txt', 'w') as test_file:
    test_file.writelines(str_list)
