
def get_float_input(prompt):
    """Get a float input from the user."""
    while True:
        user_input = input(prompt)
        try:
            return float(user_input)
        except ValueError:
            print("Invalid input. Please enter a float.")


def get_integer_input(prompt):
    """Get an integer input from the user."""
    while True:
        user_input = input(prompt)
        try:
            return int(user_input)
        except ValueError:
            print("Invalid input. Please enter an integer.")
