import extract 
import os
import pandas as pd
# import openpyxl

def transform_data():
    raw_dfs = extract.extract_data()
    # Perform transformation logic here
    raw_dfs['gs_inv']



    return raw_dfs  


dfs = transform_data()
gs_df = dfs['gs_inv']

base = os.path.dirname(os.path.abspath(__file__))
gs_df.to_excel(os.path.join(base, 'gs_invoice.xlsx'), index=False)