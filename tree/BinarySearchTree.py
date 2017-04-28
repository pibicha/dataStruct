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


class TreeNode:
    def __init__(self, key, value, left=None, right=None, parent=None):
        self.key = key
        self.value = value
        self.leftChild = left
        self.rightChild = right
        self.parent = parent

    def hasleftChild(self):
        return self.leftChild

    def hasRightChild(self):
        return self.rightChild

    def isRoot(self):
        return not self.parent

    def isLeaf(self):
        return not (self.rightChild or self.leftChild)


