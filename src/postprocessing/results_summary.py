import pandas as pd
import numpy as np

class results:
    def __init__(self, column_names):
        self.data = pd.DataFrame(columns=column_names)
        
    def append_row(self,row_name,arr):
        arr_pd = pd.DataFrame()
        self.data.loc[row_name, :] = arr

    def append_column(self,column_name, arr):
        arr_pd = pd.DataFrame()
        self.data.loc[:,column_name] = arr
