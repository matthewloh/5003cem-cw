from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Iterable

from pos_entities import Order
import datetime as dt
from pos_constants import TIMEFMT, DATEFMT, DATE_WITH_TIMEFMT


@dataclass
class Node:
    unixTimestamp: int
    item: Order
    left: Node | None = None
    right: Node | None = None
    parent: Node | None = None

    @property
    def is_right(self) -> bool:
        return bool(self.parent and self is self.parent.right)


@dataclass
class BinarySearchTree:
    root: Node | None = None

    def __reassign_nodes(self, node: Node, new_children: Node | None) -> None:
        if new_children is not None:  # reset its kids
            new_children.parent = node.parent
        if node.parent is not None:  # reset its parent
            if node.is_right:  # If it is the right child
                node.parent.right = new_children
            else:
                node.parent.left = new_children
        else:
            self.root = new_children

    def is_empty(self) -> bool:
        return not self.root

    def insert(self, timeInUnix: int, item: Order) -> None:
        new_node = Node(timeInUnix, item)  # create new node
        if self.is_empty():  # if BST is empty
            self.root = new_node
        else:
            parent = self.root
            if parent is None:
                return
            while True:  # Traverse until leaf
                if timeInUnix < parent.unixTimestamp:  # traverse left
                    if parent.left is None:  # Parent is leaf
                        parent.left = new_node  # insert new node as left child
                        break
                    else:
                        parent = parent.left  # continue traversing
                else:
                    if parent.right is None:
                        parent.right = new_node
                        break
                    else:
                        parent = parent.right
            new_node.parent = parent  # set parent of new node
            # while curr != None:  # traversal until leaf
            #     par = curr  # lagging behind
            #     if data < curr.item:
            #         curr = curr.left
            #     elif data > curr.item:
            #         curr = curr.right
            #     else:
            #         return False  # no allow duplicate value insert

            # if data < par.item:  # par points to the leaf node
            #     par.left = newNode  # insert as left child
            # else:
            #     par.right = newNode  # insert as right child
        # return True

    def batch_insert(self, orders: list[Order]) -> None:
        for order in orders:
            self.insert(order.unixTimestamp, order)

    def search_by_date_and_time(self, timeInUnix: int) -> Node | None:
        """ 
        Search for the node with the specified value and return it.
        """
        if self.is_empty():
            raise IndexError("BST is empty")
        curr = self.root
        while curr is not None and curr.unixTimestamp != timeInUnix:
            curr = curr.left if timeInUnix < curr.unixTimestamp else curr.right
        return curr

    def search_by_order_id(self, order_id: int) -> Node | None:
        """ 
        Search for the node with the specified value and return it.
        """
        if self.is_empty():
            raise IndexError("BST is empty")
        curr = self.root
        while curr is not None and curr.item.order_id != order_id:
            curr = curr.left if order_id < curr.item.order_id else curr.right
        return curr

    def get_most_forward_in_time(self, node: Node | None = None) -> Node | None:
        """
        Go through the BST and return the Order object farthest in the future. (i.e. the largest unixTimestamp).
        Go deep on the right side of the BST.
        """
        if node is None:
            if self.root is None:
                return None
            node = self.root

        while node.right is not None:
            node = node.right

        return node

    def get_most_backward_in_time(self, node: Node | None = None) -> Node | None:
        """
        Go through the BST and return the Order object farthest in the past. (i.e. the smallest unixTimestamp).
        Go deep on the left side of the BST.
        """
        if node is None:
            if self.root is None:
                return None
            node = self.root

        while node.left is not None:
            node = node.left

        return node

    def remove_by_date_and_time(self, timeInUnix: int) -> bool:
        """ 
        Remove the node with the specified value and return its Order object. 
        """
        if self.is_empty():
            raise IndexError("BST is empty")
        node = self.search_by_date_and_time(timeInUnix)
        if node is None:
            return False
        return self.remove(node)

    def remove_by_order_id(self, order_id: int) -> bool:
        """ 
        Remove the node with the specified value and return its Order object. 
        """
        if self.is_empty():
            raise IndexError("BST is empty")
        node = self.search_by_order_id(order_id)
        if node is None:
            return False
        return self.remove(node)

    def remove(self, unixTimestamp: int) -> Node | None:
        node = self.search_by_date_and_time(unixTimestamp)
        if node is None:
            msg = f"Node with unixTimestamp {dt.datetime.fromtimestamp(unixTimestamp).strftime(DATE_WITH_TIMEFMT)} not found"
            raise ValueError(msg)
        if node.left is None and node.right is None:
            self.__reassign_nodes(node, None)
        elif node.left is None:
            self.__reassign_nodes(node, node.right)
        elif node.right is None:
            self.__reassign_nodes(node, node.left)
        else:
            tmp_node = self.get_most_forward_in_time(node.left)
            self.remove_by_date_and_time(tmp_node.unixTimestamp)
            node.unixTimestamp = tmp_node.unixTimestamp
            node.item = tmp_node.item
        # if self.__root == None:  # if BST is empty
        #     return False

        # curr = self.__root
        # par = None
        # found = False

        # while curr != None:  # traversal until leaf
        #     if data == curr.item:
        #         found = True
        #         break
        #     par = curr
        #     if data < curr.item:
        #         curr = curr.left
        #     else:
        #         curr = curr.right

        # if not found:
        #     return False

        # # Case 1: Node has no children
        # if curr.left == None and curr.right == None:
        #     if curr != self.__root:
        #         if par.left == curr:
        #             par.left = None
        #         else:
        #             par.right = None
        #     else:
        #         self.__root = None

        # # Case 2: Node has one child
        # elif curr.leftChild == None:
        #     if curr != self.__root:
        #         if par.left == curr:
        #             par.left = curr.rightChild
        #         else:
        #             par.right = curr.rightChild
        #     else:
        #         self.__root = curr.rightChild

        # elif curr.rightChild == None:
        #     if curr != self.__root:
        #         if par.left == curr:
        #             par.left = curr.leftChild
        #         else:
        #             par.right = curr.leftChild
        #     else:
        #         self.__root = curr.leftChild

        # # Case 3: Node has two children
        # else:
        #     replace = curr.rightChild
        #     while replace.leftChild != None:
        #         replace = replace.leftChild

        #     curr.item = replace.item
        #     self.__remove(replace.item)

        # self.__numOfItem -= 1
        # return True

    def preorder_traverse(self, node: Node | None) -> Iterable:
        if node is not None:
            yield node  # Preorder Traversal
            yield from self.preorder_traverse(node.left)
            yield from self.preorder_traverse(node.right)

    def traversal_tree(self, traversal_function=None) -> Any:
        """
        This function traversal the tree.
        You can pass a function to traversal the tree as needed by client code
        """
        if traversal_function is None:
            return self.preorder_traverse(self.root)
        else:
            return traversal_function(self.root)

    def inorder(self, arr: list, node: Node | None) -> None:
        """Perform an inorder traversal and append values of the nodes to
        a list named arr"""
        if node:
            self.inorder(arr, node.left)
            arr.append(node.item)
            self.inorder(arr, node.right)

    def find_kth_smallest(self, k: int, node: Node) -> int:
        """Return the kth smallest element in a binary search tree"""
        arr: list[int] = []
        # append all values to list using inorder traversal
        self.inorder(arr, node)
        return arr[k - 1]


def inorder(curr_node: Node | None) -> list[Node]:
    """
    inorder (left, self, right)
    """
    node_list = []
    if curr_node is not None:
        node_list = inorder(curr_node.left) + \
            [curr_node] + inorder(curr_node.right)
    return node_list


def postorder(curr_node: Node | None) -> list[Node]:
    """
    postOrder (left, right, self)
    """
    node_list = []
    if curr_node is not None:
        node_list = postorder(curr_node.left) + \
            postorder(curr_node.right) + [curr_node]
    return node_list


if __name__ == "__main__":
    myBst = BinarySearchTree()
    # Write a program to ask user to enter 10 numbers and insert into a BST
    # Call the function displayBST to display the content of BST in inOrder traversal.

    for i in range(10):
        myBst.insert(int(input("Enter a number: ")))
    # 57, 40, 10, 13, 36, 71, 95 , 105, 69, 79
    myBst.displayBST()
    myBst.displayAll()
