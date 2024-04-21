import numpy as np


class Matrix:
    matrix = []  # static attribute

    @classmethod
    def generate_matrix(cls, n, m):
        cls.matrix = np.array([[np.random.randint(1, 10) for _ in range(m)] for _ in range(n)])
        return cls.matrix

    @staticmethod
    def print_matrix(matrix):
        for row in matrix:
            for col in row:
                print(col, end=' ')
            print()

    @staticmethod
    def insert_line(matrix, line, index):
        return np.insert(matrix, index, line, axis=0)

    @staticmethod
    def find_line_with_min_element(matrix):
        min_value = np.min(matrix)
        min_index = np.argwhere(matrix == min_value)[0][1]
        return min_index

    @staticmethod
    def insert_first_line_after_line_with_min_element(matrix):
        index = Matrix.find_line_with_min_element(matrix)
        return Matrix.insert_line(matrix, matrix[0], index + 1)

    @staticmethod
    def calculate_median_of_first_row_numpy(matrix):
        return np.median(matrix[0])

    @staticmethod
    def calculate_median_of_first_row_formula(matrix):
        sorted_row = np.sort(matrix[0])
        n = len(sorted_row)
        if n % 2 == 1:
            return sorted_row[n // 2]
        else:
            return (sorted_row[n // 2 - 1] + sorted_row[n // 2]) / 2
