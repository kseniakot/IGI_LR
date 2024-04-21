import os
import numpy as np
from task5.Matrix import Matrix
from Services.InputService import InputService
from menu.menu import wait_for_key_press


def test_numpy():
    """Test numpy functions."""

    # Create array of a specific type
    # Create an array of all zeros
    print("Create an array of all zeros")
    zeros = np.zeros((3, 3))
    print(zeros)

    # Create an array of all ones
    print("Create an array of all ones")
    ones = np.ones((3, 3))
    print(ones)

    # Create a 3x3 identity matrix
    print("Create a 3x3 identity matrix")
    identity = np.eye(3)
    print(identity)

    # Create an array with random values
    print("Create an array with random values")
    random = np.random.random((3, 3))
    print(random)

    # Indexing and slicing numpy arrays
    arr = np.array([[1, 2, 3], [4, 5, 6], [7, 8, 9]])
    # Full slice
    print("Full slice")
    print(arr[:])
    # Slice the first dimension (selects the first row)
    print("Select the first row")
    print(arr[0])
    # Slice multiple dimensions (selects the first element from the first row)
    print("The first element from the first row")
    print(arr[0, 0])
    # Slice with steps (selects every second element from the first row)
    print("Every second element from the first row")
    print(arr[0, ::2])
    # Slice a sub-matrix (selects the first two elements from the first two rows)
    print("The first two elements from the first two rows")
    print(arr[:2, :2])
    # Slice a single column as a 1D array (selects the first column)
    print("The first column as a 1D array")
    print(arr[:, 0])

    # Slice a single column as a 2D array (selects the first column)
    print("The first column as a 2D array")
    print(arr[:, 0:1])

    # Universal functions in numpy
    a = np.array([1, 2, 3, 4])
    b = np.array([5, 6, 7, 8])
    print("Test universal functions in numpy")
    print(a)
    print(b)
    c = np.add(a, b)
    print("Add element by element: ", c)

    d = np.multiply(a, b)
    print("Multiply element by element: ", d)

    e = np.sqrt(a)
    print("Sqrt: ", e)

    f = np.sin(a)
    print("Sin: ", f)

    g = np.log(a)
    print("Natural log:", g)


def test_numpy_math():
    """Work with math and statistics."""
    # Calculate the mean of an array
    a = np.array([1, 2, 3, 4, 5])
    print("First array", a)
    mean = np.mean(a)
    print("Mean: ", mean)

    # Calculate the median of an array
    median = np.median(a)
    print("Median: ", median)

    # Calculate the standard deviation of an array
    std = np.std(a)
    print("Standard deviation: ", std)

    # Calculate the variance of an array
    var = np.var(a)
    print("Variance: ", var)

    # Calculate the correlation coefficient between two arrays
    b = np.array([5, 4, 3, 2, 1])
    print("Second array", b)
    correlation = np.corrcoef(a, b)
    print("Correlation coefficient: ", correlation)


def task_5():
    os.system('clear')
    # Get the number of rows and columns
    n = InputService.get_integer_input("Enter the number of rows: ")
    while n <= 0:
        print("The number of rows must be a positive integer.")
        n = InputService.get_integer_input("Enter the number of rows: ")

    m = InputService.get_integer_input("Enter the number of columns: ")
    while m <= 0:
        print("The number of columns must be a positive integer.")
        m = InputService.get_integer_input("Enter the number of columns: ")

        # Generate a matrix
    matrix = Matrix.generate_matrix(n, m)
    print("\nGenerated matrix:")
    Matrix.print_matrix(matrix)
    # Paste the first row after the row that contains the minimum element
    matrix = Matrix.insert_first_line_after_line_with_min_element(matrix)
    print("\nMatrix after inserting the first row after the row that contains the minimum element:")
    Matrix.print_matrix(matrix)

    # Calculate the median of the first row using the numpy function
    median_numpy = Matrix.calculate_median_of_first_row_numpy(matrix)
    print(f"\nMedian of the first row using numpy: {median_numpy}")

    # Calculate the median of the first row using the formula
    median_formula = Matrix.calculate_median_of_first_row_formula(matrix)
    print(f"Median of the first row using the formula: {median_formula}")

    # Work with numpy
    print("Test numpy")
    test_numpy()

    # Work with math and statistics
    print("Test math and statistics")
    test_numpy_math()
    wait_for_key_press()


if __name__ == '__main__':
    task_5()
