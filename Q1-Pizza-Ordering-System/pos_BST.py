from __future__ import annotations

from dataclasses import dataclass
from typing import List

from pos_entities import Order
import datetime as dt
from pos_constants import DATE_WITH_TIMEFMT, NOTSET


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

    def rearrange_nodes(self, node: Node, new_children: Node | None) -> None:
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

    def get_left_and_right_of_root(self) -> tuple[Node | None, Node | None]:
        """
        Get the left and right nodes of the root.
        """
        return (self.root.left, self.root.right)

    def get_a_node_using_today(
        self,
        customerId: int,
        orderId: int,
    ) -> Node | None:
        """
        Traverse as you would a linear list, because we don't know if the node is on the left or right side of the BST.
        """
        customerId = int(customerId)
        orderId = int(orderId)
        # Root is always None Customer and None Order, so just skip it
        curr = self.root.left
        if curr is None:  # BST has no added nodes (left)
            return None
        elif (
            curr.item.customer.id == customerId and curr.item.order_id == orderId
        ):  # it itself is the node
            return curr
        elif (
            curr.item.customer.id != customerId and curr.item.order_id != orderId
        ):  # it itself is not the node
            while curr is not None:  # traverse left
                if (
                    curr.item.customer.id == customerId
                    and curr.item.order_id == orderId
                ):
                    return curr
                curr = curr.right  # traverse right
        else:  # it itself is not the node
            while curr is not None:  # traverse right
                if (
                    curr.item.customer.id == customerId
                    and curr.item.order_id == orderId
                ):
                    return curr
                curr = curr.left

    def go_before_today_until_customerId_or_orderId(
        self,
        customerId: int,
        orderId: int,
    ) -> Node | None:
        """
        Returns a node where the customerId or orderId matches the specified values.
        The node returned is obtained by going through the left side of the BST.
        Requires either customerId or orderId to be specified.
        """
        customerId = int(customerId)
        orderId = int(orderId)
        curr = self.root.left
        if curr is None:
            return None
        # print(type(curr.item.customer.id), type(customerId))
        # print(type(curr.item.order_id), type(orderId))
        # <class 'int'> <class 'str'>
        # <class 'int'> <class 'str'>
        if curr.item.customer.id == customerId and curr.item.order_id == orderId:
            return curr
        else:
            while curr is not None:
                if (
                    curr.item.customer.id == customerId
                    and curr.item.order_id == orderId
                ):
                    return curr
                curr = curr.left

    def go_after_today_until_customerId_or_orderId(
        self,
        customerId: str | int = NOTSET,
        orderId: str | int = NOTSET,
    ) -> Node | None:
        """
        View order details using today's date.
        Requires either customerId or orderId to be specified.
        """
        customerId = int(customerId)
        orderId = int(orderId)
        curr = self.root.right
        if curr is None:
            return None
        if curr.item.customer.id == customerId and curr.item.order_id == orderId:
            return curr
        else:
            while curr is not None:
                if (
                    curr.item.customer.id == customerId
                    and curr.item.order_id == orderId
                ):
                    return curr
                curr = curr.right

    def view_order_details_by_order_id(self, orderId: int) -> Node | None:
        """
        View order details using today's date.
        """
        orderId = int(orderId)
        # Do an exhaustive search on the left and right side of the BST
        # because we don't know if the node is on the left or right side of the BST.
        curr = self.root.left
        if curr is None:
            return None
        if curr.item.order_id == orderId:
            return curr
        else:
            while curr is not None:
                if curr.item.order_id == orderId:
                    return curr
                curr = curr.right
        curr = self.root.right
        if curr is None:
            return None
        if curr.item.order_id == orderId:
            return curr
        else:
            while curr is not None:
                if curr.item.order_id == orderId:
                    return curr
                curr = curr.right

    def view_order_details_by_customer_id(self, customerId: int) -> List[Node] | None:
        """
        View order details using today's date.
        Returns a list of nodes where the customerId matches the specified value.
        """
        found_nodes = []
        customerId = int(customerId)
        curr = self.root.left
        if curr is None:
            return None
        if curr.item.customer.id == customerId:
            found_nodes.append(curr)
        # Traverse until leaf on both sides of the BST
        while curr is not None:
            if curr.item.customer.id == customerId:
                found_nodes.append(curr)
            curr = curr.left
        curr = self.root.right
        if curr is None:
            return None
        if curr.item.customer.id == customerId:
            found_nodes.append(curr)
        while curr is not None:
            if curr.item.customer.id == customerId:
                found_nodes.append(curr)
            curr = curr.right
        return found_nodes

    def load_node_details(self, node: Node) -> None:
        pizzas = node.item.pizzas
        pizzaMsg = ""
        toppingInfo = ""
        for i, pizza in list(enumerate(pizzas)):
            pizzaMsg += f"""
Pizza {i + 1}:
Pizza ID: {pizza.pizza_code}
Pizza Size: {pizza.size}
Pizza Toppings: {toppingInfo}
Pizza Price: RM{pizza.unit_price}
"""
            for ing, qty in pizza.toppings.items():
                toppingInfo += f"{ing}: {qty}\n"
        msg = f"""
Viewing order details for order ID {node.item.order_id}:        
|~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~|
Customer ID: {node.item.customer.id}
Customer Name: {node.item.customer.name}
Customer Address: {node.item.customer.address}

Pizza(s):
{pizzaMsg}
|~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~|
[1] Update Order
[2] Delete Order
[3] Back
"""
        print(msg)
        while True:
            choice = input("Enter your choice: ")
            if choice == "1":
                self.update_node_pizza(node)
                break
            elif choice == "2":
                self.delete_node(node)
                break
            elif choice == "3":
                break
            else:
                print("Invalid choice. Please try again.")

    def update_node_pizza(self, node: Node) -> None:
        pizzas = node.item.pizzas
        pizzaMsg = ""
        toppingInfo = ""
        for i, pizza in list(enumerate(pizzas)):
            for ing, qty in pizza.toppings.items():
                toppingInfo += f"{ing}: {qty}\n"
            pizzaMsg += f"""
Pizza {i + 1}:
Pizza ID: {pizza.pizza_code}
Pizza Size: {pizza.size}
Pizza Toppings: {toppingInfo}
Pizza Price: RM{pizza.unit_price}
"""
        msg = f"""
Viewing pizzas for order ID {node.item.order_id}:
{pizzaMsg}
|~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~|
[1] Modify Pizza Size
[2] Delete Pizza
[3] Back
"""
        print(msg)
        while True:
            choice = input("Enter your choice: ")
            if choice == "1":
                self.modify_pizza(node)
            elif choice == "2":
                self.delete_pizza(node)
            elif choice == "3":
                break
            else:
                print("Invalid choice. Please try again.")

    def modify_pizza(self, node: Node) -> None:
        pizzas = node.item.pizzas
        whichPizza = int(input("Which pizza do you want to modify? "))
        if whichPizza > len(pizzas):
            print("Invalid pizza number.")
            return
        pizza = pizzas[whichPizza - 1]
        print(
            f"""
Pizza {whichPizza}:
Pizza ID: {pizza.pizza_code}
Pizza Size: {pizza.size}
Pizza Toppings: {pizza.toppings}
Pizza Price: RM{pizza.unit_price}
"""
        )
        while True:
            choice = input("Enter your choice: ")
            if choice == "1":
                print("MODIFY PIZZA SIZE")
                size = input("Enter pizza size (Small/Large): ")
                pizza.size = size
                print("Pizza size updated.")
                break
            elif choice == "2":
                print("MODIFY PIZZA TOPPINGS")
                print("Current pizza toppings:")
                print(pizza.toppings)
                topping = input("Enter topping to add: ")
                qty = int(input("Enter quantity: "))
                pizza.toppings[topping] = qty
                print("Pizza toppings updated.")
                break
            elif choice == "3":
                break
            else:
                print("Invalid choice. Please try again.")

    def delete_pizza(self, node: Node) -> None:
        pizzas = node.item.pizzas
        whichPizza = int(input("Which pizza do you want to delete? "))
        if whichPizza > len(pizzas):
            print("Invalid pizza number.")
            return
        pizza = pizzas[whichPizza - 1]
        print(
            f"""
Pizza {whichPizza}:
Pizza ID: {pizza.pizza_code}
Pizza Size: {pizza.size}
Pizza Toppings: {pizza.toppings}
Pizza Price: RM{pizza.unit_price}
"""
        )
        while True:
            print("Are you sure you want to delete this pizza?")
            print("[1] Yes")
            print("[2] No")
            choice = input("Enter your choice: ")
            if choice == "1":
                node.item.pizzas.remove(pizza)
                print("Pizza deleted.")
                break
            elif choice == "2":
                break
            else:
                print("Invalid choice. Please try again.")

    def delete_node(self, node: Node) -> None:
        self.remove(node)
        print("Order deleted.")

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

    def remove(self, node: Node) -> Node | None:
        unixTimestamp = node.unixTimestamp
        if node is None:
            msg = f"Node with unixTimestamp {dt.datetime.fromtimestamp(unixTimestamp).strftime(DATE_WITH_TIMEFMT)} not found"
            raise ValueError(msg)
        if node.left is None and node.right is None:
            self.rearrange_nodes(node, None)
        elif node.left is None:
            self.rearrange_nodes(node, node.right)
        elif node.right is None:
            self.rearrange_nodes(node, node.left)
        else:
            tmp_node = self.get_most_forward_in_time(node.left)
            self.remove(tmp_node)
            tmp_node.left = node.left
            tmp_node.right = node.right
            self.rearrange_nodes(node, tmp_node)
