from dataclasses import dataclass, field
import time as time_obj
from typing import Dict, List
import datetime as dt
from pos_constants import *
from pos_entities import Customer, Pizza, Order
from pos_BST import BinarySearchTree, Node


@dataclass
class PizzaOrderingSystemCLI:
    BST: BinarySearchTree = field(default_factory=BinarySearchTree)
    order_id: int = 0
    customer_id: int = 0
    customPizzaCount: int = 1

    def init_current_node(self) -> None:
        currentTime = time_obj.time()
        strTime = dt.datetime.fromtimestamp(currentTime).strftime(TIMEFMT)
        strDate = dt.datetime.fromtimestamp(currentTime).strftime(DATEFMT)
        print(strTime, strDate)
        item = Order(
            unixTimestamp=int(currentTime), order_id=69, pizzas=[], customer=None
        )
        current_node = Node(unixTimestamp=int(currentTime), item=item)
        self.BST.root = current_node

    def display_welcome_art(self) -> None:
        msg = f"""
._________________________________________________________________________.
|  ____ _________ ____ ____ ____ ____ ____ _________ ____ ____ ____ ____  |
| || A |||       |||P |||i |||z |||z |||a |||       |||C |||a |||k |||e | |
| ||___|||_______|||__|||__|||__|||__|||__|||_______|||__|||__|||__|||__| |
| |/___\|/_______\|/__\|/__\|/__\|/__\|/__\|/_______\|/__\|/__\|/__\|/__\ | 
._________________________________________________________________________.
"""
        print("=" * 75, end="")
        print(msg, end="")
        print("=" * 75)

    def display_options(self) -> None:
        self.display_welcome_art()
        print("Pizza Ordering System")
        print("1. Place an order")
        print("2. Search for an order to modify/delete")
        print("3. View most forward and backward in time")
        print("4. Exit")

    def place_order(self) -> None:
        print("When would you like to place your order? (q to cancel)")
        date = input(
            "Enter date or leave blank for today (dd/mm/yyyy): ").strip()
        if date == "":
            date = dt.datetime.fromtimestamp(time_obj.time()).strftime(DATEFMT)
        elif date == "q":
            print("Exit")
            return
        time = (
            input(
                "Enter time (hh:mma) or leave blank for current time, e.g: 12:00AM, 12:00PM: "
            )
            .strip()
            .replace(" AM", "AM")
            .replace(" PM", "PM")
            .upper()
        )
        if time == "":
            time = dt.datetime.fromtimestamp(time_obj.time()).strftime(TIMEFMT)
        validation = False
        while not validation:
            try:
                time_obj.strptime(f"{date} {time}", DATE_WITH_TIMEFMT)
                validation = True
            except ValueError:
                print("Invalid date or time format")
                date = input(
                    "Enter date or leave blank for today (dd/mm/yyyy): "
                ).strip()
                if date == "":
                    date = dt.datetime.fromtimestamp(
                        time_obj.time()).strftime(DATEFMT)
                time = (
                    input(
                        "Enter time (hh:mma) or leave blank for current time, e.g: 12:00AM, 12:00PM: "
                    )
                    .strip()
                    .replace(" AM", "AM")
                    .replace(" PM", "PM")
                    .upper()
                )
                if time == "":
                    time = dt.datetime.fromtimestamp(
                        time_obj.time()).strftime(TIMEFMT)
        unixTimestamp = int(
            time_obj.mktime(time_obj.strptime(
                f"{date} {time}", DATE_WITH_TIMEFMT))
        )
        print(unixTimestamp)
        dateTime = dt.datetime.fromtimestamp(unixTimestamp)
        print(dateTime.strftime(DATE_WITH_TIMEFMT))
        print("How many pizzas would you like to order?")
        num_pizzas = int(input("Enter number of pizzas: "))
        self.pizzaList: List[Pizza] = []
        self.pizzaNum = 0
        self.display_pizza_options(num_pizzas=num_pizzas)
        name = input("Enter name: ")
        address = input("Enter address: ")
        contact_number = input("Enter contact number: ")
        order = Order(
            unixTimestamp=unixTimestamp,
            order_id=self.order_id,
            pizzas=self.pizzaList,
            customer=Customer(
                id=self.customer_id,
                name=name,
                address=address,
                contact_number=contact_number,
            ),
        )
        self.BST.insert(timeInUnix=unixTimestamp, item=order)
        allPizzas = ""
        for pizza in self.pizzaList:
            allPizzas += f"{pizza.pizza_code} - {pizza.toppings} - {pizza.size} - {pizza.unit_price} \n"
        successMsg = f"""
._________________________________________________________________________.
|  ____ _________ ____ ____ ____ ____ ____ _________ ____ ____ ____ ____  |
| || A |||       |||P |||i |||z |||z |||a |||       |||C |||a |||k |||e | |
| ||___|||_______|||__|||__|||__|||__|||__|||_______|||__|||__|||__|||__| |
| |/___\|/_______\|/__\|/__\|/__\|/__\|/__\|/_______\|/__\|/__\|/__\|/__\ |
|~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~|
|  Your order has been placed!                                            |
|  Here are your order details:                                           |
|~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~|
   Order ID: {self.order_id}
   Customer ID: {self.customer_id}                                        
   Name: {name}                                                           
   Address: {address}                                                     
   Contact Number: {contact_number}                                       
   Order Date and Time: {dateTime.strftime(DATE_WITH_TIMEFMT)}            
   Order Amount: {order.display_order_amount()}                           
   Pizzas:                                                                
{allPizzas}                                                            
|  Thank you for ordering with us!                                        |
|  Please come again!                                                     |
._________________________________________________________________________.

"""
        print(successMsg)
        ask = input("Would you like to log out from this customerId? (y/n): ")
        if ask == "y":
            self.customer_id += 1
        self.order_id += 1

    def display_pizza_options(self, num_pizzas: int) -> None:
        while True and self.pizzaNum < num_pizzas:
            msg = f"""
Pizza {self.pizzaNum + 1} / {num_pizzas}
.___________________________________________________________________________.
|  Pizza Menu - Type the number of the pizza you would like to order.       |
|  [1] Pepperoni Pizza - Pepperoni, Cheese(x2) -------------------- RM15.00 |
|  [2] Hawaiian Pizza - Ham, Pineapple, Cheese -------------------- RM12.00 | 
|  [3] Vegetarian Pizza - Mushroom, Onion, Capsicum, Cheese ------- RM09.00 |
|  [4] Custom Pizza                                                         |
|                                                           [q] Cancel      |
|                                                           [w] View Pizzas |
.___________________________________________________________________________.
"""
            print(msg)
            choice = input("Enter your choice: ")
            if choice == "1":
                newPizza = Pizza(
                    pizza_code=f"PEP_{self.order_id}-{self.pizzaNum}",
                    toppings={PEPPERONI: 1, CHEESE: 2},
                    size=LARGE,
                    unit_price=15.00,
                )
                self.pizzaList.append(newPizza)
                self.pizzaNum += 1
            elif choice == "2":
                newPizza = Pizza(
                    pizza_code=f"HAW_{self.order_id}-{self.pizzaNum}",
                    toppings={HAM: 1, PINEAPPLE: 1, CHEESE: 1},
                    size=LARGE,
                    unit_price=12.00,
                )
                self.pizzaList.append(newPizza)
                self.pizzaNum += 1
            elif choice == "3":
                newPizza = Pizza(
                    pizza_code=f"VEG_{self.order_id}-{self.pizzaNum}",
                    toppings={MUSHROOM: 1, ONION: 1, CAPSICUM: 1, CHEESE: 1},
                    size=LARGE,
                    unit_price=9.00,
                )
                self.pizzaList.append(newPizza)
                self.pizzaNum += 1
            elif choice == "4":
                self.customPizzaId = f"CUS{self.order_id}-{self.customPizzaCount}"
                totalToppings = int(
                    input("How many toppings would you like to add? "))
                self.toppingOptions = {}
                self.toppingNum = 0
                for i in range(totalToppings):
                    self.display_topping_options(totalToppings=totalToppings)
                price = self.get_custom_pizza_price()
                newPizza = Pizza(
                    pizza_code=self.customPizzaId,
                    toppings=self.toppingOptions,
                    size=LARGE,
                    unit_price=price,
                )
                self.pizzaList.append(newPizza)
                print(f"Custom Pizza #{self.customPizzaCount} added")
                self.customPizzaCount += 1
                self.pizzaNum += 1
            elif choice == "q":
                print("Exit")
                break
            elif choice == "w":
                print("Viewing pizzas")
                for pizza in self.pizzaList:
                    print(pizza)
            else:
                print("Invalid choice")

    def display_topping_options(self, totalToppings: int) -> List[Dict[str, int]]:
        while True and self.toppingNum < totalToppings:
            msg = f"""
Topping #{self.toppingNum + 1} / {totalToppings} 
.___________________________________________________________________________.
|  Topping Menu - Type the number of the topping you would like to add.     |
|  Topping ------------------------------------------------- Price per Unit |
|  [1] Cheese -------------------------------------------------------RM5.00 |
|  [2] Pepperoni ----------------------------------------------------RM5.00 |
|  [3] Ham --------------------------------------------------------- RM4.00 | 
|  [4] Pineapple ----------------------------------------------------RM3.00 |
|  [q] Mushroom -----------------------------------------------------RM2.00 |
|  [w] Onion --------------------------------------------------------RM1.00 |
|  [e] Capsicum -----------------------------------------------------RM1.00 |
|                                                                           |
|                                                     [z] Reset             |
|                                                     [x] List all Toppings |
|                                                     [c] Cancel            |
.___________________________________________________________________________.
"""
            print(msg)
            choice = input("Enter your choice: ")
            if choice == "1":
                self.add_topping_option(CHEESE)
            elif choice == "2":
                self.add_topping_option(PEPPERONI)
            elif choice == "3":
                self.add_topping_option(HAM)
            elif choice == "4":
                self.add_topping_option(PINEAPPLE)
            elif choice == "q":
                self.add_topping_option(MUSHROOM)
            elif choice == "w":
                self.add_topping_option(ONION)
            elif choice == "e":
                self.add_topping_option(CAPSICUM)
            elif choice == "z":
                self.reset_topping_options()
            elif choice == "x":
                self.list_topping_options()
            elif choice == "c":
                print("Exit")
                break
            else:
                print("Invalid choice")

    def add_topping_option(self, topping: str) -> None:
        if topping in self.toppingOptions:
            self.toppingOptions[topping] += 1
        else:
            self.toppingOptions[topping] = 1
        self.toppingNum += 1

    def get_custom_pizza_price(self) -> float:
        total = 0
        for topping, qty in self.toppingOptions.items():
            if topping == CHEESE or topping == PEPPERONI:
                total += 5.00 * qty
            elif topping == HAM:
                total += 4.00 * qty
            elif topping == PINEAPPLE:
                total += 3.00 * qty
            elif topping == MUSHROOM:
                total += 2.00 * qty
            elif topping == ONION or topping == CAPSICUM:
                total += 1.00 * qty
        return total

    def list_topping_options(self) -> None:
        print("Current toppings:")
        for topping, qty in self.toppingOptions.items():
            print(f"{topping} - {qty}")

    def reset_topping_options(self) -> None:
        self.toppingOptions = {}
        self.toppingNum = 0

    def view_order_details_by_date(self) -> None:
        self.currentRootDate = dt.datetime.fromtimestamp(
            self.BST.root.item.unixTimestamp
        ).strftime(DATE_WITH_TIMEFMT)
        self.currentCustomerId = NOTSET
        self.currentOrderId = NOTSET
        self.timeStampToSearch = NOTSET
        self.searchedForDate = NOTSET
        while True:
            msg = f"""
|~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~|
    Current Root Date: {self.currentRootDate + f" - {self.BST.root.item.unixTimestamp}"} 
    Searched For Date: {self.searchedForDate}                              
    Current Customer ID: {self.currentCustomerId} 
    Current Order ID: {self.currentOrderId}                                 
|___________________________________________________________________________|
|  Options to obtain your order                                             |
|                                                                           |
|  [1] No date specified - Search exhaustively ~O(n) time complexity        |
|  [2] Before today - Get your order if it was placed before today ~O(log n)| 
|  [3] After today - Get your order if it was placed after today ~O(log n)  | 
|  [q] Get an order by order id                                             |
|  [w] Get order(s) by using your customerId                                |
|  [z] Enter my customerId and/or orderId                                   | 
|  [e] Reset my customerId and/or orderId                                   |
|                                                                [c] Cancel |
.___________________________________________________________________________. 
"""
            print(msg)
            choice = input("Enter your choice (c to exit): ")
            if choice == "1":
                print("Searching linearly")
                node = self.BST.get_a_node_using_today(
                    customerId=self.currentCustomerId,
                    orderId=self.currentOrderId,
                )
                self.BST.load_node_details(
                    node) if node else print("Order not found")
            elif choice == "2":
                print("Searching orders before today")
                node = self.BST.go_before_today_until_customerId_or_orderId(
                    customerId=self.currentCustomerId, orderId=self.currentOrderId
                )
                self.BST.load_node_details(
                    node) if node else print("Order not found")
            elif choice == "3":
                print("Searching orders after today")
                node = self.BST.go_after_today_until_customerId_or_orderId(
                    customerId=self.currentCustomerId, orderId=self.currentOrderId
                )
                self.BST.load_node_details(
                    node) if node else print("Order not found")
            elif choice == "q":
                print("View order by order id")
                self.BST.view_order_details_by_order_id(
                    orderId=self.currentOrderId)
            elif choice == "w":
                print("Viewing order(s) by customer id")
                self.BST.view_order_details_by_customer_id(
                    customerId=self.currentCustomerId
                )
            elif choice == "z":
                print("Inputting customer id and order id")
                customerId = input("Enter customer id: ")
                orderId = input("Enter order id: ")
                self.currentCustomerId = customerId
                self.currentOrderId = orderId
            elif choice == "z":
                while True:
                    print(
                        "Inputting customer id and order id (leave blank if not known)"
                    )
                    customerId = input("Enter customer id: ")
                    orderId = input("Enter order id: ")
                    if orderId == "" and customerId != "":
                        self.currentOrderId = NOTSET
                        self.currentCustomerId = customerId
                        break
                    elif customerId == "" and orderId != "":
                        self.currentCustomerId = NOTSET
                        self.currentOrderId = orderId
                        break
                    elif orderId == "" and customerId == "":
                        self.currentCustomerId = NOTSET
                        self.currentOrderId = NOTSET
                        print("Both order id and customer id are blank")
                        break
                    else:
                        self.currentCustomerId = customerId
                        self.currentOrderId = orderId
                        break
            elif choice == "c":
                print("Exit")
                return
            else:
                print("Invalid choice")


def main():
    cli = PizzaOrderingSystemCLI()
    cli.init_current_node()
    while True:
        cli.display_options()
        choice = int(input("Enter your choice: "))
        if choice == 1:
            cli.place_order()
        elif choice == 2:
            cli.view_order_details_by_date()
        elif choice == 3:
            print("Getting most forward in time")
            print(cli.BST.get_most_forward_in_time(cli.BST.root))
            print("Getting most backward in time")
            print(cli.BST.get_most_backward_in_time(cli.BST.root))
        elif choice == 4:
            print("Exit")
            break
        else:
            print("Invalid choice")


if __name__ == "__main__":
    main()
