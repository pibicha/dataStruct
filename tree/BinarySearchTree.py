"""
二叉搜索树结构上和堆挺像，不过二叉树不一定是完全二叉树；
而且二叉树的每个节点，其左节点都小于本身，右节点都大于本身；
至少需要两个实体；树、节点
"""


class BinarySearchTree:
    def __init__(self):
        self.root = None
        self.size = 0

    def length(self):
        return self.size

    def __len__(self):
        return self.size

    def __iter__(self):
        return self.root.__iter__()

    # setitem 可以像 map[2] = "dsf" 一样赋值
    def __setitem__(self, key, value):
        self.put(key, value)

    # 插入时，需要递归寻找合适的位置
    def put(self, key, value):
        # 如果树中已有节点，则需要递归寻找合适的位置插入
        if self.root:
            # 一个方法做一件事，找位置的事由searchSeat实现
            self.searchSeat(key, value, self.root)

        # 如果树中还没有节点，直接插入根节点
        else:
            self.root = TreeNode(key, value)

    # 根据key和currentNode的值，判断key、value需要往左还是右插入
    def searchSeat(self, key, value, currentNode):
        # key小于当前节点的key
        if key < currentNode.key:
            # 情况一：当前节点已有左节点，那么需要从其左节点继续向下按同样的方式查找
            if currentNode.hasLeftChild():
                self.searchSeat(key, value, currentNode.leftChild)
            else:  # 情况二 ：当前节点没有左节点，直接将key、value设为其左节点
                currentNode.leftChild = TreeNode(key, value, parent=currentNode)

        # key大于当前节点的key
        else:
            # 情况一：当前节点已有右节点，那么需要从其右节点继续向下按同样的方式查找
            if currentNode.hasRightChild():
                self.searchSeat(key, value, currentNode)
            else:
                currentNode.rightChild = TreeNode(key, value, currentNode)

    # 实现一个方法，通过key，获得其对应的value值
    def get(self, key):
        # （编程习惯）双重否定加深了语义复杂度，尽量避免。。
        # # 若树没有节点，直接返回None
        # if not self.root:
        #     return None
        # else: # 有节点的话，从传入的key开始往下找

        if self.root:  # 若树不为空，则递归往下找
            node = self.searchValue(key, self.root)
            if node:
                return node.value
            else:
                return None
        else:
            return None

    def searchValue(self, key, currentNode):
        if not currentNode:
            return None
        elif currentNode.key == key:
            return currentNode
        elif key < currentNode.key:
            return self.searchValue(key, currentNode.leftChild)
        else:
            return self.searchValue(key, currentNode.rightChild)

    def __getitem__(self, key):
        return self.get(key)

    # 实现in操作 这里操作的是key
    def __contains__(self, item):
        if self.searchValue(item, self.root):
            return True
        else:
            return False

    """
    对于删除，先考虑节点的情况
    1，树中只有一个节点
    2，是叶子节点；直接删除，也不会影响树的结构（平衡树和红黑树就会有影响了）
    3，有子节点不为空；这种情况比较麻烦，考虑其节点情况
    3.1，待删除的节点有左右两个节点，这种情况稍微复杂，使用辅助函数，
    3.2，待删除的节点，只有一个子结点，那么将独子放到删除节点的位置

    基于以上情况，需要在TreeNode中，新增几个判断节点的子节点情况的方法
    """

    def delete(self, key):
        if self.size == 1 and self.root.key == key:
            self.root = None
            self.size -= 1
        elif self.size > 1:
            needRemove = self.searchSeat(key, self.root)
            if needRemove:
                self.remove(needRemove)
                self.size -= 1
            else:
                raise KeyError('key not in tree')

    def remove(self, currentNode):
        if currentNode.isLeaf():
            if currentNode.parent.leftChild == currentNode:
                currentNode.parent.leftChild = None
            else:
                currentNode.parent.rightChild = None
        """
        当前节点有两个个节点
        3.1.1
        两个子节点中，选谁来升做父节点？
        解决办法：
        1，寻找继任者
        1.1 如果节点有右子节点，则后继节点是右子树中的最小的键。
        1.2 如果节点没有右子节点并且是父节点的左子节点，则父节点是后继节点。
        1.3 如果节点是其父节点的右子节点，并且它本身没有右子节点，则此节点的后继节点是其父节点的后继节点，不包括此节点。
        2，使用继任者填到删除节点的位置
        """

    # 继任者对于右树来说，是右的最小值，
    def findSuccessor(self):
        succ = None
        if self.hasRightChild():
            succ = self.rightChild.findMin()
        else:
            if self.parent:
                if self.isLeftChild():
                    succ = self.parent
                else:
                    self.parent.rightChild = None
                    succ = self.parent.findSuccessor()
                    self.parent.rightChild = self
        return succ

    def findMin(self):
        current = self
        while current.hasLeftChild():
            current = current.leftChild
        return current

    def spliceOut(self):
        if self.isLeaf():
            if self.isLeftChild():
                self.parent.leftChild = None
            else:
                self.parent.rightChild = None
        elif self.hasAnyChildren():
            if self.hasLeftChild():
                if self.isLeftChild():
                    self.parent.leftChild = self.leftChild
                else:
                    self.parent.rightChild = self.leftChild
                self.leftChild.parent = self.parent
            else:
                if self.isLeftChild():
                    self.parent.leftChild = self.rightChild
                else:
                    self.parent.rightChild = self.rightChild
                self.rightChild.parent = self.parent

    def __iter__(self):
        if self:
            if self.hasLeftChild():
                for elem in self.leftChiLd:
                    yield elem
            yield self.key
            if self.hasRightChild():
                for elem in self.rightChild:
                    yield elem


class TreeNode:
    def __init__(self, key, value, left=None, right=None, parent=None):
        self.key = key
        self.value = value
        self.leftChild = left
        self.rightChild = right
        self.parent = parent

    def hasLeftChild(self):
        return self.leftChild

    def hasRightChild(self):
        return self.rightChild

    def isRoot(self):
        return not self.parent

    def isLeaf(self):
        return not (self.rightChild or self.leftChild)

    # 删除节点所需方法
    def hasAnyChildren(self):
        return self.rightChild or self.leftChild

    def hasBothChildren(self):
        return self.rightChild and self.leftChild

    def isLeftChild(self):
        return self.parent and self.parent.leftChild == self

    def isRightChild(self):
        return self.parent and self.parent.rightChild == self


bst = BinarySearchTree()
bst.put(1, "a")
bst.put(2, "b")
print(bst[1], bst[2])
