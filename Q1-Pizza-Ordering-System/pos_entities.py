from dataclasses import dataclass, field
import typing
from typing import Dict, List, TypedDict, Union
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
    toppings: Dict[str, int] = field(default_factory=dict)
    size: str = "Large"
    unit_price: float = 0.0


@dataclass
class Order:
    unixTimestamp: int
    order_id: int
    pizzas: list[Pizza]
    customer: Customer

    def display_order_amount(self) -> float:
        total = 0
        for pizza in self.pizzas:
            total += pizza.unit_price
        return total
