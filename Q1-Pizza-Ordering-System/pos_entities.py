from dataclasses import dataclass, field
from typing import List
from datetime import date
from enum import StrEnum, auto


@dataclass
class Customer:
    id: int
    name: str
    address: str
    contact_number: str


@dataclass
class Pizza:
    pizza_code: str
    toppings: list(dict[str, float])
    size: str
    unit_price: float
    quantity: int


@dataclass
class Order:
    unixTimestamp: int
    order_id: int
    pizzas: list[Pizza]
    customer: Customer

    def display_order_amount(self) -> float:
        total = 0
        for pizza in self.pizzas:
            total += pizza.unit_price * pizza.quantity
        return total
