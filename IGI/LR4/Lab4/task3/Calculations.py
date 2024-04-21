import statistics
import matplotlib.pyplot as plt
import numpy as np
import math


class Calculations:
    """Class for calculations of the arcsin function using the power series and some statistics calculations"""
    x_sequence = []
    x_list = []
    y_list = []
    math_y_list = []

    @staticmethod
    def factorial(n):
        """Calculate the factorial of a number"""
        if n == 0:
            return 1
        else:
            return n * Calculations.factorial(n - 1)

    def arcsin(self, x, eps):
        """Calculate the value of the arcsin function using the power series"""
        n = 0
        result = 0

        term = x
        while abs(term) > eps:
            self.x_sequence.append(term)
            result += term
            n += 1
            if n > 500:
                break
            coeff = Calculations.factorial(2 * n) / (4 ** n * (Calculations.factorial(n)) ** 2)
            term = coeff * (x ** (2 * n + 1)) / (2 * n + 1)
        return result, n

    def mean(self):
        """Calculate the mean of a sequence"""
        return statistics.mean(self.x_sequence)

    def median(self):
        """Calculate the median of a sequence"""
        return statistics.median(self.x_sequence)

    def mode(self):
        """Calculate the mode of a sequence"""
        return statistics.mode(self.x_sequence)

    def variance(self):
        """Calculate the variance of a sequence"""
        return statistics.variance(self.x_sequence)

    def stdev(self):
        """Calculate the standard deviation of a sequence"""
        return statistics.stdev(self.x_sequence)

    def __prepare_data_for_graph(self):
        """Prepare data for the graph"""
        self.x_list = np.arange(-1, 1, 0.01)
        for x in self.x_list:
            self.y_list.append(self.arcsin(x, 0.001)[0])
            self.math_y_list.append(math.asin(x))

    def draw_plot(self):
        """Draw a plot of the arcsin function using the power series and the math asin function"""
        self.__prepare_data_for_graph()
        plt.plot(self.x_list, self.math_y_list, label="math.asin(x)")
        plt.plot(self.x_list, self.y_list, label="arcsin(x)")
        plt.xlabel("x")
        plt.ylabel("y")
        plt.grid(True)
        plt.legend(loc="upper left", fontsize="small")
        plt.title("arcsin(x) vs math.asin(x)")
        plt.savefig("plot.png")
        plt.show()


