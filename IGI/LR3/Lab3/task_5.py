# Task 5
# Find the product of the positive elements of the list and the sum of the elements
#  of the list located before the element with the minimum absolute value.

import os
import random
from menu import print_menu, navigate_menu, wait_for_key_press
from inits import get_integer_input


def my_generator(size):
    for _ in range(size):
        yield random.uniform(-100, 100)


def generate_list(size):
    return [x / 10 for x in my_generator(size)]


def get_list(prompt):
    while True:
        user_input = input(prompt)
        if not user_input.strip():
            print("Input cannot be empty. Please enter a list of float values.")
            continue
        try:
            return list(map(float, user_input.split()))
        except ValueError:
            print("Invalid input. Please enter a list of float values.")


def print_iterable(iterable, prompt="The sequence is: "):
    print(prompt, end=' ')
    for el in iterable:
        print(el, end=' ')
    print()


def multiply_positive(iterable):
    product = 1
    for el in iterable:
        if el > 0:
            product *= el
    return product


def task_5_enter_list():
    os.system('clear')
    user_input = get_list("Enter a list of float values separated by spaces: ")
    print_iterable(user_input)
    list_analyzer(user_input)
    wait_for_key_press()


def task_5_enter_size():
    os.system('clear')
    sz = get_integer_input("Enter the size of the list: ")
    user_sequence = generate_list(sz)
    print_iterable(user_sequence)
    list_analyzer(user_sequence)
    wait_for_key_press()


def list_analyzer(lst):
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
