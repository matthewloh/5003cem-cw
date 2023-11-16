""" 
These are the formulas used to determine the total interest, monthly interest, and monthly installment for your loan.
    Your total interest = interest rate/100 x loan amount x loan period
    Your monthly interest = total interest / (loan period x 12)
    Your monthly installment = (loan amount + total interest) / (loan period x 12)
Question 4: Concurrent process

    a) Write a function to calculate and display the car loan monthly repayment. Assume a flat interest
    rate is used.
    b) Write a program to allow users to calculate the monthly repayment for 3 different customers.
    The program should call the function defined in (a) concurrently.

Observe the output of your solution and discuss the relevant theories that are used.

Libraries used : concurrent.futures, time, random, threading
"""