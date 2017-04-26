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

    def __str__(self):
        print(self.heapList)


heap = BinHeap()
heap.insert(3)
heap.insert(2)
heap.insert(1)
heap.insert(6)
heap.insert(0)
heap.insert(4)
heap.insert(7)
heap.insert(5)

print(heap)
