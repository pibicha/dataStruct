"""
众人围一圈；从一数到七；人来又人往；逢七便出局；直至座一人；
"""

from . import MyQueue


def josheper(players, bullet=7):
    seat = MyQueue()

    # 众人围一圈
    for player in players:
        seat.enqueue(player)

    # 直至座一人(为什么最后一句反而在这~ 因为人生一开始就默默的注定在循环~ 如果没有什么来触发改变，也只能日复一日)
    while seat.size() < 1:
        # 从一数到七
        for i in range(bullet):
            # 人来又人往
            seat.enqueue(seat.dequeue())

        # 逢七便出局
        seat.dequeue()
