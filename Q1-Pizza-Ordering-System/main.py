""" 
Question 1: Pizza Ordering System
Design and develop a Pizza Ordering System based on the following requirements:
• The program should be menu driven, giving the user various choices of operation that allows the
user to:
o place an order for the pizza(s).
o View their order details.
o Modify or delete a particular order if necessary.
• For every order, the following information will be stored:
o OrderID (this should be autogenerated), Pizza Code, toppings, size, unit price, quantity
and customer information.
o The customer information should consists of customerID, name, address and contact
number.
o The system shall display additional information such as amount (unit price * quantity)
when viewing the order details.
• The program must use BST data structure to facilitate each operation.
• The system shall demonstrate a good OOP design, data validation and error handling.
"""
from typing import List
from attr import dataclass


@dataclass
class Customer:
    id: int
    name: str
    address: str
    contact_number: str


@dataclass
class PizzaOrder:
    order_id: int
    pizza_code: str
    toppings: List[str]
    size: str
    unit_price: float
    quantity: int
    customer : Customer


@dataclass
class CustomerList:
    customer_list: List[Customer]

    def __init__(self):
        self.customer_list = []

    def add(self, customer: Customer):
        self.customer_list.append(customer)
    
@dataclass
class PizzaOrderList:
    pizza_order_list: List[PizzaOrder]

    def __init__(self):
        self.pizza_order_list = []
        
    def add(self, pizza_order: PizzaOrder):
        self.pizza_order_list.append(pizza_order)

class PizzaOrderingSystem:
    def __init__(self):
        self.__customer_id = 0
        self.__order_id = 0
        self.__customer_list = List[Customer] 
        self.__pizza_order_list = List[PizzaOrder] 

    # Auto generate customer id and order id
    def __generate_customer_id(self) -> int:
        self.__customer_id += 1
        return self.__customer_id

    def __generate_order_id(self) -> int:
        self.__order_id += 1
        return self.__order_id

    def __get_customer(self, customer_id: int) -> Customer:
        for customer in self.__customer_list:
            if customer.id == customer_id:
                return customer

    def __get_order(self, order_id: int) -> PizzaOrder:
        for order in self.__pizza_order_list:
            if order.order_id == order_id:
                return order

    def __get_order_total(self, order_id: int) -> float:
        order = self.__get_order(order_id)
        return order.unit_price * order.quantity

    def __get_order_details(self, order_id: int) -> str:
        order = self.__get_order(order_id)
        customer = self.__get_customer(order.customer.id)
        return f"""
        Order ID: {order.order_id}
        Pizza Code: {order.pizza_code}
        Toppings: {order.toppings}
        Size: {order.size}
        Unit Price: {order.unit_price}
        Quantity: {order.quantity}
        Customer ID: {customer.id}
        Customer Name: {customer.name}
        Customer Address: {customer.address}
        Customer Contact Number: {customer.contact_number}
        Total: {self.__get_order_total(order.order_id)}
        """

    def __get_customer_details(self, customer_id: int) -> str:
        customer = self.__get_customer(customer_id)
        return f"""
        Customer ID: {customer.id}
        Customer Name: {customer.name}
        Customer Address: {customer.address}
        Customer Contact Number: {customer.contact_number}
        """

    def __get_customer_orders(self, customer_id: int) -> List[PizzaOrder]:
        return [
            order
            for order in self.__pizza_order_list
            if order.customer_id == customer_id
        ]

    def __get_customer_orders_details(self, customer_id: int) -> str:
        customer_orders = self.__get_customer_orders(customer_id)
        return "\n".join(
            [
                f"""
                Order ID: {order.order_id}
                Pizza Code: {order.pizza_code}
                Toppings: {order.toppings}
                Size: {order.size}
                Unit Price: {order.unit_price}
                Quantity: {order.quantity}
                Total: {self.__get_order_total(order.order_id)}
                """
                for order in customer_orders
            ]
        )

    def __get_customer_total(self, customer_id: int) -> float:
        customer_orders = self.__get_customer_orders(customer_id)
        return sum([self.__get_order_total(order.order_id) for order in customer_orders])

    def __get_customer_orders_total(self, customer_id: int) -> str:
        return f"""
        Customer ID: {customer_id}
        Customer Total: {self.__get_customer_total(customer_id)}
        """

    def __get_all_orders(self) -> List[PizzaOrder]:
        return self.__pizza_order_list

    def __get_all_orders_details(self) -> str:
        return "\n".join(
            [
                f"""
                Order ID: {order.order_id}
                Pizza Code: