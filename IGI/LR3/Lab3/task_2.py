# Task 2
# Organise cycle which takes integer numbers and calculates
#     the amount of numbers which are greater than 12
#     input 0 to stop the cycle

from menu import wait_for_key_press
from inits import get_integer_input


def number_of_elements_greater_than_12():
    x = -1
    counter = 0
    while x != 0:
        x = get_integer_input("Enter x: ")
        if x == 0:
            return counter
        elif x > 12:
            counter += 1


def task_2():
    """ Organise cycle which takes integer numbers and calculates
    the amount of numbers which are greater than 12
    input 0 to stop the cycle """

    x = -1
    print("Enter 0 to stop the cycle")
    print("The number of elements greater than 12: ", number_of_elements_greater_than_12())

    wait_for_key_press()
