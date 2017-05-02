"""
从堆到二叉搜索树，在二叉搜索树中，曾经考虑过插入，
对于子树的高度，可能会插入的复杂度为O(n)；
AVL树就能使根节点的左右子树达到平衡，AVL树在BST的基础上，
引入了平衡因子的概念；新加入的节点，balanceFactor即是0；
而其父节点，爷爷节点，到根节点，他们的balanceFactor也需要
做出相应改变；  当根结点的balanceFactor为0时，整棵树就是平衡的；
若为负数，则右树重；否则就是左树重了；当平衡因子不为0时，就要做出相应的
调整，使得树呈平衡态，才能使搜索复杂度不至于扩大到O(N)
"""


# AVL是BST的子类，这里为了逻辑方便展示，就不用继承了
# 这里只需要改造put和delete方法，使得改变树结构时，维持平衡
class AVL:
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

    # 插入节点时，需要递归调整节点所影响到的父辈
    def updateBalance(self, node):
        if node.balanceFactor > 1 or node.balanceFactor < -1:
            self.rebalance(node)
            return
        if node.parent != None:
            if node.isLeftChild():
                node.parent.balanceFactor += 1
            elif node.isRightChild():
                node.parent.balanceFactor -= 1

            if node.parent.balanceFactor != 0:
                self.updateBalance(node.parent)

    # 对子树进行旋转：一般而言，以root出发，左重右旋，右重左旋
    # 然而对于一中特殊的结构型如"<" ">"，就需要将其形状改为"/" "\" 再进行左旋 右旋
    def rebalance(self, node):
        if node.balanceFactor < 0:
            if node.rightChild.balanceFactor > 0:
                self.rotateRight(node.rightChild)
                self.rotateLeft(node)
            else:
                self.rotateLeft(node)
        elif node.balanceFactor > 0:
            if node.leftChild.balanceFactor < 0:
                self.rotateLeft(node.leftChild)
                self.rotateRight(node)
            else:
                self.rotateRight(node)

    def rotateLeft(self, rotRoot):
        newRoot = rotRoot.rightChild
        rotRoot.rightChild = newRoot.leftChild
        if newRoot.leftChild != None:
            newRoot.leftChild.parent = rotRoot
        newRoot.parent = rotRoot.parent
        if rotRoot.isRoot():
            self.root = newRoot
        else:
            if rotRoot.isLeftChild():
                rotRoot.parent.leftChild = newRoot
            else:
                rotRoot.parent.rightChild = newRoot
        newRoot.leftChild = rotRoot
        rotRoot.parent = newRoot
        rotRoot.balanceFactor = rotRoot.balanceFactor + 1 - min(newRoot.balanceFactor, 0)
        newRoot.balanceFactor = newRoot.balanceFactor + 1 + max(rotRoot.balanceFactor, 0)

    def rotateRight(self, rotRoot):
        newRoot = rotRoot.leftChild
        rotRoot.leftChild = newRoot.leftChild
        if newRoot.rightChild != None:
            newRoot.rightChild.parent = rotRoot
        newRoot.parent = rotRoot.parent
        if rotRoot.isRoot():
            self.root = newRoot
        else:
            if rotRoot.isLeftChild():
                rotRoot.parent.rightChild = newRoot
            else:
                rotRoot.parent.leftChild = newRoot
        newRoot.rightChild = rotRoot
        rotRoot.parent = newRoot
        rotRoot.balanceFactor = rotRoot.balanceFactor + 1 - min(newRoot.balanceFactor, 0)
        newRoot.balanceFactor = newRoot.balanceFactor + 1 + max(rotRoot.balanceFactor, 0)

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


        elif currentNode.hasBothChildren():
            succ = currentNode.findSuccessor()
            succ.spliceOut()
            currentNode.key = succ.key
            currentNode.payload = succ.payload

        else:
            # 待删除节点只有一个子节点
            if currentNode.hasLeftChild():
                if currentNode.isLeftChild():
                    currentNode.leftChild.parent = currentNode.parent
                    currentNode.parent.leftChild = currentNode.leftChild
                elif currentNode.isRightChild():
                    currentNode.leftChild.parent = currentNode.parent
                    currentNode.parent.rightChild = currentNode.leftChild
            else:
                if currentNode.isLeftChild():
                    currentNode.rightChild.parent = currentNode.parent
                    currentNode.parent.leftChild = currentNode.rightChild
                elif currentNode.isRightChild():
                    currentNode.rightChild.parent = currentNode.parent
                    currentNode.parent.rightChild = currentNode.rightChild
                else:
                    currentNode.replaceNodeData(currentNode.rightChild.key,
                                                currentNode.rightChild.payload,
                                                currentNode.rightChild.leftChild,
                                                currentNode.rightChild.rightChild)

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
