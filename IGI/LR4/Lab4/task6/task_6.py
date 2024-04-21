import pandas as pd
import numpy as np
from IPython.display import display


def task_6():
    # Create a DataFrame with the following data:
    ingredients_df = pd.read_csv('ingredients.csv', sep=',')
    print("Data Frame:")
    # Displaying DataFrame
    display(ingredients_df)
    print()
    # Displaying Data Frame Info
    print("Data Frame Info:")
    print(ingredients_df.info())
    print()
    # Creating Series
    series = pd.Series(ingredients_df['ing_name'].values, index=ingredients_df['ing_id'])

    # Displaying Series
    print("Series:")
    display(series)
    print()

    # Accessing elements using label
    element = series.loc['ING005']
    print("Element with label ING005: ", element)
    # Select rows by a boolean array
    element = series.loc[series.index == 'ING006']
    print("Elements with index equal to ING006: ")
    display(element)
    print()

    # Accessing elements using index
    element = series.iloc[0]
    print("Element at index 0: ", element)
    elements = series.iloc[0:3]
    print("Elements at index 0 to 2: ")
    for elem in elements:
        print(elem)
    print()
    elements = series.iloc[[0, 2]]
    print("Elements at index 0 and 2: ")
    for elem in elements:
        print(elem)
    print()

    # Working with data
    # Calculate the mean price of all drinks
    mean_price = ingredients_df['ing_price'].mean()
    print("Mean price of all drinks: ", mean_price)
    # Find the average weight of drinks that are priced below the average
    average_weight_below_mean_price = ingredients_df.loc[ingredients_df['ing_price'] < mean_price, 'ing_weight'].mean()
    print("Average weight of drinks priced below the average: ", average_weight_below_mean_price)


if __name__ == '__main__':
    task_6()
