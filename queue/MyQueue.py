"""
python中的Queue更像是java的LinkedBlokingQueue;
这里用的Queue功能更单一一些，只需要先进先出的功能即可；
内部使用List做容器；
"""


class MyQueue:
    def __init__(self):
        self.item = []

    def enqueue(self, item):
        self.item.insert(0, item)

    def dequeue(self):
        return self.item.pop()

    def size(self):
        return len(self.item)

    def isEmpty(self):
        return 0 == len(self.item)
