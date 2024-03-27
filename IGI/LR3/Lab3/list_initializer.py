import random


def my_generator(size):
    """Generate a sequence of random float numbers."""
    for _ in range(size):
        yield random.uniform(-100, 100)


def generate_list(generator):
    """Generate a list of random float numbers."""
    return [x / 10 for x in generator]


def get_list(prompt):
    """Get a list of float values from the user."""
    while True:
        user_input = input(prompt)
        if not user_input.strip():
            print("Input cannot be empty. Please enter a list of float values.")
            continue
        try:
            return list(map(float, user_input.split()))
        except ValueError:
            print("Invalid input. Please enter a list of float values.")
