import matplotlib.pyplot as plt
import numpy as np
from task4.figure import Figure
from task4.color import Color


class Triangle(Figure):

    def __init__(self, a, h, color):
        """Initializes a Triangle object with base, height and color."""
        super().__init__("Triangle")
        self.a = a
        self.h = h
        self.color = Color(color)

    def area(self):
        """Calculates the area of a Triangle object."""
        return 0.5 * self.a * self.h

    def get_name(self):
        """Returns the name of the Triangle object."""
        return self.name

    def __str__(self):
        """Returns a string representation of the Triangle object."""
        return "{} with base {} and height {} and color {}".format(self.name, self.a, self.h, self.color.color)

    def draw_triangle(self, title):
        """Draws a Triangle object."""
        vertices = np.array([[0, 0], [self.a / 2, self.h], [self.a, 0]])
        triangle = plt.Polygon(vertices, color=self.color.color)
        plt.gca().add_patch(triangle)
        plt.xlim(-1, self.a + 1)
        plt.ylim(-1, self.h + 1)
        plt.xlabel('a')
        plt.ylabel('h')
        plt.savefig("task4/triangle.png")
        plt.title(title)
        plt.show()















