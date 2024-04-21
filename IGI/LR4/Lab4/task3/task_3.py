from prettytable import PrettyTable
from math import asin
from task3.Calculations import Calculations
from Services.InputService import InputService


def task_3():
    """Calculate the value of the arcsin function using the power series"""
    # Get x from the user
    x = InputService.get_float_input("Enter x: ")
    while not -1 <= x <= 1:
        print("The value of x must be in the range of -1 to 1")
        x = InputService.get_float_input("Enter x: ")
    # Get eps from the user
    eps = InputService.get_float_input("Enter eps: ")
    while not 0 <= eps <= 1:
        print("Epsilon must be greater than 0 and less than 1")
        eps = InputService.get_float_input("Enter eps: ")

    # Print result in a table
    calc = Calculations()
    my_table = PrettyTable(["x", "n", "F(x)", "Math F(x)", "eps"])
    my_table.add_row([x, calc.arcsin(x, eps)[1], calc.arcsin(x, eps)[0], asin(x), eps])
    print(my_table)

    # Print mean, median, mode, variance, and standard deviation
    my_table = PrettyTable(["Mean", "Median", "Mode", "Variance", "Standard Deviation"])
    my_table.add_row([calc.mean(), calc.median(), calc.mode(), calc.variance(), calc.stdev()])
    print(my_table)

    # Graph
    calc.draw_plot()


if __name__ == "__main__":
    task_3()
