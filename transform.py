import extract 
import os
# import pandas as pd
import openpyxl

def transform_data():
    raw_dfs = extract.extract_data()


    # Perform transformation logic here

    return raw_dfs  


dfs = transform_data()
print(type(dfs['gs_inv']))

# dfs['gs_inv'].info()
base = os.path.dirname(os.path.abspath(__file__))
dfs['gs_inv'].to_excel(os.path.join(base, 'gs_sales_invoice.xlsx'), index=False)
# dfs['gs_inv'].to_excel("test.xlsx", index=False)
