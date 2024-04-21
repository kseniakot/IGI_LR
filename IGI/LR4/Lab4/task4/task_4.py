import os
from math import sqrt
from matplotlib import colors as mcolors
from Services.InputService import InputService
from task4.Triangle import Triangle
from menu.menu import wait_for_key_press


def task_4():
    """Task 4: Create a class Triangle with the following methods:"""
    os.system('clear')
    input_service = InputService()

    a = InputService.get_integer_input("Enter base for the triangle: ")
    while a <= 0:
        print("Base must be greater than 0.")
        a = InputService.get_integer_input("Enter base for the triangle: ")

    h = InputService.get_integer_input("Enter height for the triangle: ")
    while h <= 0:
        print("Height must be greater than 0.")
        h = InputService.get_integer_input("Enter height for the triangle: ")

    color = input("Enter color for the triangle: ")
    while color not in mcolors.CSS4_COLORS:
        print("Invalid color name. Please enter a valid color name.")
        color = input("Enter color for the triangle: ")

    side = sqrt((a / 2) ** 2 + h ** 2)

    # Check if the triangle can be formed
    if a + side > side and a + side > a and side + side > a:
        print("A triangle can be formed.")
        triangle = Triangle(a, h, color)
        print("The area of the triangle is: {}".format(triangle.area()))
        title = input("Enter the title for the triangle: ")
        triangle.draw_triangle(title)
    else:
        print("A triangle cannot be formed.")

    wait_for_key_press()


if __name__ == "__main__":
    task_4()
