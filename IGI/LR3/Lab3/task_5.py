# Task 5
# Find the product of the positive elements of the list and the sum of the elements
#  of the list located before the element with the minimum absolute value.

import os
from menu import print_menu, navigate_menu, wait_for_key_press
from input import get_integer_input
from list_initializer import my_generator, generate_list, get_list


def print_iterable(iterable, prompt="The sequence is: "):
    """Print the elements of an iterable."""
    print(prompt, end=' ')
    for el in iterable:
        print(el, end=' ')
    print()


def multiply_positive(iterable):
    """Find the product of the positive elements of the list."""
    product = 1
    for el in iterable:
        if el > 0:
            product *= el
    return product


def task_5_enter_list():
    """Get a list of float values from the user and analyze it."""
    os.system('clear')
    user_input = get_list("Enter a list of float values separated by spaces: ")
    print_iterable(user_input)
    list_analyzer(user_input)
    wait_for_key_press()


def task_5_enter_size():
    """Generate a list of random float values and analyze it."""
    os.system('clear')
    sz = get_integer_input("Enter the size of the list: ")
    user_sequence = generate_list(my_generator(sz))
    print_iterable(user_sequence)
    list_analyzer(user_sequence)
    wait_for_key_press()


def list_analyzer(lst):
    """Analyze the list."""
    print(f"The product of the positive elements of the list: {multiply_positive(lst)}")
    print(f"The sum of the elements of the list located before the element"
          f" with the minimum absolute value: {sum(lst[:lst.index(min(lst, key=abs))])}")


def task_5():
    """Find the product of the positive elements of the list and the sum of the elements
     of the list located before the element with the minimum absolute value."""

    os.system('clear')

    prompt = '\t\t\t\tWhat would you like to do?'
    tasks = {
        "Set size": task_5_enter_size,
        "Enter list": task_5_enter_list,
    }
    options = list(tasks.keys()) + ["Exit"]
    choice = 1

    print_menu(choice, options, prompt)
    navigate_menu(choice, options, prompt, tasks)
