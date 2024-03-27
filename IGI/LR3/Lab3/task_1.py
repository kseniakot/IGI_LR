# Task 1
# Сalculate the value of a function using the function's expansion
# into a power series


import os
from math import asin
from prettytable import PrettyTable
from input import get_float_input, get_integer_input
from menu import wait_for_key_press


def factorial(n):
    """Calculate the factorial of a number"""
    if n == 0:
        return 1
    else:
        return n * factorial(n - 1)


def arcsin(x, eps):
    """Calculate the value of the arcsin function using the power series"""
    n = 0
    result = 0
    term = x
    while abs(term) > eps:
        result += term
        n += 1
        coeff = factorial(2 * n) / (4 ** n * (factorial(n)) ** 2)
        term = coeff * (x ** (2 * n + 1)) / (2 * n + 1)
    return result, n


def task_1():
    """ Сalculate the value of a function using the function's expansion
    into a power series """

    os.system('clear')

    x = get_float_input("Enter x: ")
    while not -1 <= x <= 1:
        print("The value of x must be in the range of -1 to 1")
        x = get_float_input("Enter x: ")

    eps = get_float_input("Enter eps: ")
    while not 0 <= eps <= 1:
        print("Epsilon must be greater than 0 and less than 1")
        eps = get_float_input("Enter eps: ")

    my_table = PrettyTable(["x", "n", "F(x)", "Math F(x)", "eps"])
    my_table.add_row([x, arcsin(x, eps)[1], arcsin(x, eps)[0], asin(x), eps])
    print(my_table)
    wait_for_key_press()
