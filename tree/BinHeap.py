"""
堆是完整二叉树~
完整二叉树找我的理解,就是左右子树高度差最大为一的树~
节点和子节点的大小关系不像二叉树那样严谨，只要比子节点大/小就行；
由于二叉树的节点和子节点的大小关系不是很严谨，只需要数组就能表示；
第1个元素是0(占位)，其他元素的父节点，即heap[e.index//2]
"""


class BinHeap:
    def __init__(self):
        self.heapList = [0]
        self.currentSize = 0

    def insert(self, e):
        self.heapList.append(e)
        self.currentSize = self.currentSize + 1
        # 新插入的元素，需要保证与父节点的性质
        self.up(self.currentSize)

    """
    新增的元素可以直接插入List尾部，不过这可能会导致堆的大小特性失效
    所以插入元素后，需要对新节点及其根节点进行比较，看是否需要交换~(递归)
    另外，python的交换不用引入第三方变量 或是使用亦或 ，好方便！！~~
    """

    def up(self, index):
        while index // 2 > 0:
            if self.heapList[index] < self.heapList[index // 2]:
                self.heapList[index], self.heapList[index // 2] = self.heapList[index // 2], self.heapList[index]
            index = index // 2

    """
    由于列表中第二个元素就是最小值(小顶堆)，所以删除最小值，只需要
    删除[1]元素；
    对于缺少顶部的堆，需要找到列表中最小的一个值来做堆顶，但是就算用
    找到最小值，将其作为堆顶，也会导致其原先所在的节点不平衡；
    这里暂时没想到其他的什么方法，能重建堆的方法：
    1) 将数组的最后一个值挪到[2]上
    2) 递归处理新堆顶是否需要和子节点交换
    """

    def popTop(self):
        # 1)
        top = self.heapList.pop(1)
        self.heapList.insert(1, self.heapList.pop())
        self.currentSize -= 1
        # 2)
        self.down(1)
        return top

    def down(self, index):
        while index * 2 <= self.currentSize:
            # 2.1) 节点是否与子节点交换位子，其实只要和较小的一个子节点比较即可"""
            minIndex = self.minChildIndex(index)
            if self.heapList[index] > self.heapList[minIndex]:
                self.heapList[index], self.heapList[minIndex] = self.heapList[minIndex], self.heapList[index]
            index = minIndex

    def minChildIndex(self, index):
        if index * 2 + 1 > self.currentSize:
            return index * 2
        else:
            if self.heapList[index * 2] < self.heapList[index * 2 + 1]:
                return index * 2
            else:
                return index * 2 + 1

    def __repr__(self):
        print(self.heapList)

    # 在测试时，每次都要单独insert，好麻烦；所以实现一个build方法，传入List可以构建BinHeap
    def buildheap(self, list):
        # 方案一，一个个insert，不过这样每次插入都要考虑上浮。。。
        # 方案二，整个list一次性构建成堆，然后考虑堆的性质
        # 这里使用方案二，从叶子节点的父节点，开始下沉，依次到根节点，便可保证堆的性质
        self.currentSize = len(list)
        self.heapList = [0] + list[:]
        index = self.currentSize // 2
        while index > 0:
            self.down(index)
            index -= 1


# Test
import random


def test():
    binHeap = BinHeap()
    list = []
    for i in range(1, 7):
        list.append(random.randint(1, 20))
    binHeap.buildheap(list)
    print(binHeap)


test()
