import sys
import psutil
print("psutil", psutil.Process().memory_info().rss)

test_tuple = (1, 3, 4)
test_str=str(test_tuple)
# for element in test_tuple:
#     test_str+=str(element)
print test_str

print sys.platform
print("psutil", psutil.Process().memory_info().rss)