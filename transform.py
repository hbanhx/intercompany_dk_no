from sys import prefix

import extract 
import os
import pandas as pd
# import openpyxl

def prefix_columns(raw_dfs):
    # Add prefixes to columns to avoid naming conflicts during merges
    prefixed_dfs = { key: df.add_prefix(f"{key}_") for key, df in raw_dfs.items() }
    return prefixed_dfs

def merge_invoice(df1, df2):
        # merge the two DataFrames on the specified columns, using an outer join to keep all records
        merged_df = pd.merge(
            df1, 
            df2, 
            left_on=['gs_inv_No_', 'gs_inv_Sales Invoice Line#Line No_'], 
            right_on=['pn_inv_Order No_', 'pn_inv_Sales Invoice Line#Line No_'], 
            how='outer',
            indicator=True
        )
        return merged_df

def merge_credit_memo(df1, df2):
        # merge the two DataFrames on the specified columns, using an outer join to keep all records
        merged_df = pd.merge(
            df1, 
            df2, 
            left_on=['gs_cm_No_', 'gs_cm_Sales Cr_Memo Line#Line No_'], 
            right_on=['pn_cm_Pre-Assigned No_', 'pn_cm_Sales Cr_Memo Line#Line No_'], 
            how='outer',
            indicator=True
        )
        return merged_df

def transform_data():
    # Transformation pipeline

    # Extract data using the extract module
    raw_dfs = extract.extract_data()

    # Add prefixes to columns to avoid naming conflicts during merges
    raw_dfs = prefix_columns(raw_dfs)
    print(raw_dfs.keys())

    # Merge invoices and credit memos
    inv_df = merge_invoice(raw_dfs['gs_inv'], raw_dfs['pn_inv'])
    cm_df = merge_credit_memo(raw_dfs['gs_cm'], raw_dfs['pn_cm'])

    return inv_df, cm_df


inv_df, cm_df = transform_data()

base = os.path.dirname(os.path.abspath(__file__))
inv_df.to_excel(os.path.join(base, 'gs_invoice.xlsx'), index=False)
cm_df.to_excel(os.path.join(base, 'gs_credit_memo.xlsx'), index=False)