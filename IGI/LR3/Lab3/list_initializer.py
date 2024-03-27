import random


def my_generator(size):
    """Generate a sequence of random float numbers."""
    for _ in range(size):
        yield random.uniform(-100, 100)


def generate_list(generator):
    """Generate a list of random float numbers."""
    return [x / 10 for x in generator]
