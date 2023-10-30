import queue


class TreeNode:
    def __init__(self, data):
        self.item = data
        self.leftChild = None
        self.rightChild = None


class BST:
    def __init__(self):
        self.__root = None
        self.__numOfItem = 0

    def size(self):
        return self.__numOfItem

    def search(self, data):
        if self.__root == None:  # if BST is empty
            return False
        curr = self.__root
        while curr != data:
            if data < curr.item and curr.leftChild != None:
                curr = curr.leftChild
            elif data > curr.item and curr.rightChild != None:
                curr = curr.rightChild
            else:
                return False
        return True
        # to be completed

    def __insert(self, data):
        newNode = TreeNode(data)  # create new Node
        if self.__root == None:  # if BST is empty
            self.__root = newNode
        else:
            curr = self.__root
            par = None
            while curr != None:  # traversal until leaf
                par = curr  # lagging behind
                if data < curr.item:
                    curr = curr.leftChild
                elif data > curr.item:
                    curr = curr.rightChild
                else:
                    return False  # no allow duplicate value insert

            if data < par.item:  # par points to the leaf node
                par.leftChild = newNode  # insert as left child
            else:
                par.rightChild = newNode  # insert as right child
        self.__numOfItem += 1
        return True

    def insert(self, *values):
        for value in values:
            self.__insert(value)

    def __remove(self, data):
        if self.__root == None:  # if BST is empty
            return False

        curr = self.__root
        par = None
        found = False

        while curr != None:  # traversal until leaf
            if data == curr.item:
                found = True
                break
            par = curr
            if data < curr.item:
                curr = curr.leftChild
            else:
                curr = curr.rightChild

        if not found:
            return False

        # Case 1: Node has no children
        if curr.leftChild == None and curr.rightChild == None:
            if curr != self.__root:
                if par.leftChild == curr:
                    par.leftChild = None
                else:
                    par.rightChild = None
            else:
                self.__root = None

        # Case 2: Node has one child
        elif curr.leftChild == None:
            if curr != self.__root:
                if par.leftChild == curr:
                    par.leftChild = curr.rightChild
                else:
                    par.rightChild = curr.rightChild
            else:
                self.__root = curr.rightChild

        elif curr.rightChild == None:
            if curr != self.__root:
                if par.leftChild == curr:
                    par.leftChild = curr.leftChild
                else:
                    par.rightChild = curr.leftChild
            else:
                self.__root = curr.leftChild

        # Case 3: Node has two children
        else:
            replace = curr.rightChild
            while replace.leftChild != None:
                replace = replace.leftChild

            curr.item = replace.item
            self.__remove(replace.item)

        self.__numOfItem -= 1
        return True

    def displayAll(self):
        print("Preorder: ")
        self.__preOrder(self.__root)
        print("Inorder: ")
        self.__inOrder(self.__root)
        print("Postorder: ")
        self.__postOrder(self.__root)
        # print("Breadth First Traversal:")
        # self.__levelOrder()

    def __levelOrder(self):  # BFS

        if (self.__root == None):
            return

        q = queue.Queue(self.__numOfItem)
        q.put(self.__root)

        while (not q.empty()):
            curr = q.get()
            print(curr.item, " ")

            if (curr.leftChild):
                q.put(curr.leftChild)

            if (curr.rightChild):
                q.put(curr.rightChild)

    def __preOrder(self, TreeNode):  # N L R
        if TreeNode == None:
            return
        print(TreeNode.item)
        self.__preOrder(TreeNode.leftChild)
        self.__preOrder(TreeNode.rightChild)

    def __inOrder(self, TreeNode):  # L N R
        if TreeNode == None:
            return
        self.__inOrder(TreeNode.leftChild)
        print(TreeNode.item)
        self.__inOrder(TreeNode.rightChild)

    def __postOrder(self, TreeNode):  # L R N
        if TreeNode == None:
            return
        self.__postOrder(TreeNode.leftChild)
        self.__postOrder(TreeNode.rightChild)
        print(TreeNode.item)

    def displayBST(self):
        self.__displayBST(self.__root, 0)

    def __displayBST(self, TreeNode, level):
        if TreeNode == None:
            return
        self.__displayBST(TreeNode.rightChild, level + 1)
        print("     " * level, TreeNode.item)
        self.__displayBST(TreeNode.leftChild, level + 1)


if __name__ == "__main__":
    myBst = BST()
    # Write a program to ask user to enter 10 numbers and insert into a BST
    # Call the function displayBST to display the content of BST in inOrder traversal.

    for i in range(10):
        myBst.insert(int(input("Enter a number: ")))
    # 57, 40, 10, 13, 36, 71, 95 , 105, 69, 79
    myBst.displayBST()
    myBst.displayAll()
