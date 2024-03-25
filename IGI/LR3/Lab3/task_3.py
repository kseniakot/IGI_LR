# Task 3
# Check if the string is a binary string

import os
from menu import wait_for_key_press


def is_binary_string(s):
    return all(char in '01' for char in s)


def task_3():
    """ Check if the string is a binary string """
    os.system('clear')
    check_str = input("Enter a string: ")
    if is_binary_string(check_str):
        print("The string is a binary string")
    else:
        print("The string is not a binary string")

    wait_for_key_press()
    return
