"""
快排~
1，于无序数组a中；寻一中轴p；
2，将a中元素较p小的元素置于lower列表，大于则置于greater列表
3，重复1，2 步骤
4，设定终止条件
"""


def quicksort(array):
    # 4，设定终止条件
    if len(array) <= 1:
        return array
    lower = []
    greater = []
    # 1 于无序数组a中；寻一中轴p；
    p = array.pop()
    # 2 将a中元素较p小的元素置于lower列表，大于则置于greater列表
    for e in array:
        if e < p:
            lower.append(e)
        else:
            greater.append(e)
    # 3，重复1，2 步骤
    return quicksort(lower) + [p] + quicksort(greater)


# Test

import random

array = []
for i in range(20):
    array.append(random.randint(-50, 50))

print(array)
sorted = quicksort(array)
print(sorted)
