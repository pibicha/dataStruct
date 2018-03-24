"""
众人围一圈:
1 从一数到七；2 人来又人往；3 逢七便出局；4 直至座一人；
"""


# fixme 用队列来实现还是有些混淆，用循环队列解决试试

def josheper(players, bullet=7):
    seat = MyQueue()

    # 众人围一圈
    for player in players:
        print('玩家%s进入圈内' % player)
        seat.enqueue(player)

    # 直至座一人(为什么最后一句反而在这:结束即开始)
    while seat.size() > 1:
        # 从一数到七
        for i in range(bullet):
            # 人来又人往
            dequeue = seat.dequeue()
            print('玩家%s从圈尾出局并插入首位' % dequeue)
            seat.enqueue(dequeue)

            # 逢七便出局
        out = seat.dequeue()
        print("玩家【%s】不幸为第%s号" % (out, bullet))

    return seat.dequeue()

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
        return self.item == []



print('最终存活：%s' % josheper(["张三", "李四", "王二", "麻子", "韩梅梅", "李芳芳"]))


