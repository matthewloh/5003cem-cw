import threading
from dataclasses import dataclass
from typing import Iterable, Dict

import threading

CUSTOMER_DATA = [
    {"id": 1, "loan_amount": 10000, "loan_period": 2, "interest_rate": 5},
    {"id": 2, "loan_amount": 15000, "loan_period": 3, "interest_rate": 6},
    {"id": 3, "loan_amount": 20000, "loan_period": 4, "interest_rate": 7},
]
# Function to calculate and display car loan monthly repayment


def calculate_monthly_repayment(customer_id: int, loan_amount: int, loan_period: int, interest_rate: int):
    # Calculate total interest
    total_interest = (interest_rate / 100) * loan_amount * loan_period

    # Calculate monthly interest
    monthly_interest = total_interest / (loan_period * 12)

    # Calculate monthly installment
    monthly_installment = (loan_amount + total_interest) / (loan_period * 12)

    # Display results
    print(f"Customer {customer_id}:")
    print(f"Total Interest: {total_interest}")
    print(f"Monthly Interest: {monthly_interest}")
    print(f"Monthly Installment: {monthly_installment}\n")

# Function to get user input and call the calculate_monthly_repayment function


def process_data():
    threads = []

    # Loop through customer data and create threads
    for customer in CUSTOMER_DATA:
        thread = threading.Thread(target=calculate_monthly_repayment, args=(
            customer["id"], customer["loan_amount"], customer["loan_period"], customer["interest_rate"]
        ))
        threads.append(thread)

    # Start all threads
    for thread in threads:
        thread.start()

    # Wait for all threads to finish
    for thread in threads:
        thread.join()


# Call the main function
process_data()

CUSTOMER_DATA = [
    {"id": 1, "loan_amount": 10000, "loan_period": 2, "interest_rate": 5},
    {"id": 2, "loan_amount": 15000, "loan_period": 3, "interest_rate": 6},
    {"id": 3, "loan_amount": 20000, "loan_period": 4, "interest_rate": 7},
]
for customer in CUSTOMER_DATA:
    calculate_monthly_repayment(
        customer["id"], customer["loan_amount"], customer["loan_period"], customer["interest_rate"])
