import pandas as pd
import numpy as np

cars_df = pd.read_csv('gcar_data.csv', sep=',')
print(cars_df.to_string())
