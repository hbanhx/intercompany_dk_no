# from sys import prefix
import extract 
import os
import pandas as pd
# import openpyxl


def columns_mapping():
    mapping = {
        # GS invoice
        "invoice_gs_Posting Date": "Posting Date GS",
        "invoice_gs_No_": "Document No. GS",
        "invoice_gs_Order No_": "Order No. GS",
        "invoice_gs_Sell-to Customer No_": "Customer No. GS",
        "invoice_gs_Sell-to Customer Name": "Customer Name GS",
        "invoice_gs_External Document No_": "External Document No. GS",
        "invoice_gs_Currency Code": "Currency GS",
        "invoice_gs_Sales Invoice Line#Amount": "Amount GS",
        "invoice_gs_Sales Invoice Line#Amount Including VAT": "Amount Including VAT GS",
        "invoice_gs_doc_type": "Document Type GS",

        # PN invoice
        "invoice_pn_Posting Date": "Posting Date PN",
        "invoice_pn_No_": "Document No. PN",
        "invoice_pn_Order No_": "Order No. PN",
        "invoice_pn_Sell-to Customer No_": "Customer No. PN",
        "invoice_pn_Sell-to Customer Name": "Customer Name PN",
        "invoice_pn_External Document No_": "External Document No. PN",
        "invoice_pn_Currency Code": "Currency PN",
        "invoice_pn_Sales Invoice Line#Amount": "Amount PN",
        "invoice_pn_Sales Invoice Line#Amount Including VAT": "Amount Including VAT PN",
        "invoice_pn_doc_type": "Document Type PN",

        # GS credit memo
        "credit_memo_gs_Posting Date": "Posting Date GS",
        "credit_memo_gs_No_": "Document No. GS",
        "credit_memo_gs_Pre-Assigned No_": "Order No. GS",
        "credit_memo_gs_Sell-to Customer No_": "Customer No. GS",
        "credit_memo_gs_Sell-to Customer Name": "Customer Name GS",
        "credit_memo_gs_External Document No_": "External Document No. GS",
        "credit_memo_gs_Currency Code": "Currency GS",
        "credit_memo_gs_Sales Cr_Memo Line#Amount": "Amount GS",
        "credit_memo_gs_Sales Cr_Memo Line#Amount Including VAT": "Amount Including VAT GS",
        "credit_memo_gs_doc_type": "Document Type GS",

        # PN credit memo
        "credit_memo_pn_Posting Date": "Posting Date PN",
        "credit_memo_pn_No_": "Document No. PN",
        "credit_memo_pn_Pre-Assigned No_": "Order No. PN",
        "credit_memo_pn_Sell-to Customer No_": "Customer No. PN",
        "credit_memo_pn_Sell-to Customer Name": "Customer Name PN",
        "credit_memo_pn_External Document No_": "External Document No. PN",
        "credit_memo_pn_Currency Code": "Currency PN",
        "credit_memo_pn_Sales Cr_Memo Line#Amount": "Amount PN",
        "credit_memo_pn_Sales Cr_Memo Line#Amount Including VAT": "Amount Including VAT PN",
        "credit_memo_pn_doc_type": "Document Type PN"
    }
    return mapping

def filter_columns(df):
    columns = []
    for column in columns_mapping().values():
        if column in df.columns and column not in columns:
            columns.append(column)
    if '_merge' in df.columns:
        columns.append('_merge')  
    return columns


def merge_documents(gs_df, pn_df, doc_type):
    # Merge GS and PN DataFrames based on document type (invoice or credit memo)

    # Add document type column to identify whether the record is an invoice or credit memo
    gs_df["doc_type"] = doc_type
    pn_df["doc_type"] = doc_type

    # prefix columns to avoid naming conflicts during merges
    gs = gs_df.add_prefix(f"{doc_type}_gs_")
    pn = pn_df.add_prefix(f"{doc_type}_pn_")

    # Merge keys for invoices and credit memos
    if doc_type == "invoice":
        left_keys  = ['invoice_gs_No_', 'invoice_gs_Sales Invoice Line#Line No_']
        right_keys = ['invoice_pn_Order No_', 'invoice_pn_Sales Invoice Line#Line No_']

    elif doc_type == "credit_memo":
        left_keys  = ['credit_memo_gs_No_', 'credit_memo_gs_Sales Cr_Memo Line#Line No_']
        right_keys = ['credit_memo_pn_Pre-Assigned No_', 'credit_memo_pn_Sales Cr_Memo Line#Line No_']

    # Merge GS + PN
    merged_df = pd.merge(
        gs,
        pn,
        left_on=left_keys,
        right_on=right_keys,
        how="outer",
        indicator=True
    )
    return merged_df

def concatenate_dataframes(df1, df2):
    # concatenate the two DataFrames vertically
    concatenated_df = pd.concat([df1, df2], ignore_index=True)
    return concatenated_df

def vat_reconciliation(df1, df2):
    # Reconcile VAT amounts between invoices and credit memos

    # Rename columns for clarity
    vat_inv_df = df1.rename(columns=columns_mapping())
    vat_cm_df = df2.rename(columns=columns_mapping())




    # Select relevant columns for the final output (optional, can be adjusted based on requirements)
    vat_inv_columns = filter_columns(vat_inv_df)
    vat_cm_columns = filter_columns(vat_cm_df)  

    # Ensure the selected columns are in the correct order and exist in the DataFrames
    vat_inv_df = vat_inv_df[vat_inv_columns]
    vat_cm_df = vat_cm_df[vat_cm_columns]
    vat_df = pd.concat([vat_inv_df, vat_cm_df], ignore_index=True)

    return vat_df

    # MAKE UNIFIED VAT COLUMNS
# def vat_reconciliation(df1, df2):
#     df1 = df1.rename(columns=columns_mapping())
#     df2 = df2.rename(columns=columns_mapping())

#     unified_columns = []
#     for col in columns_mapping().values():
#         if col in df1.columns or col in df2.columns:
#             if col not in unified_columns:
#                 unified_columns.append(col)

#     if "_merge" in df1.columns or "_merge" in df2.columns:
#         unified_columns.append("_merge")

#     df1 = df1.reindex(columns=unified_columns)
#     df2 = df2.reindex(columns=unified_columns)

#     return pd.concat([df1, df2], ignore_index=True)



def transform_data():
    # Transformation pipeline

    # Extract data using the extract module
    raw_dfs = extract.extract_data()

    # Merge invoices and credit memos from both company codes
    inv_df = merge_documents(raw_dfs['gs_inv'], raw_dfs['pn_inv'], 'invoice')
    cm_df = merge_documents(raw_dfs['gs_cm'], raw_dfs['pn_cm'], 'credit_memo')

    # Concatenate the merged DataFrames to create a unified dataset
    concatenated_df = concatenate_dataframes(inv_df, cm_df)

    # Perform VAT reconciliation
    vat_df = vat_reconciliation(df1=inv_df, df2=cm_df)

    # New intercompany transaction for posting
    # TODO: Create a new DataFrame for intercompany transactions based on the reconciled VAT data and other relevant fields


    return inv_df, cm_df, concatenated_df, vat_df



inv_df, cm_df, concatenated_df, vat_df = transform_data()

base = os.path.dirname(os.path.abspath(__file__))
inv_df.to_excel(os.path.join(base, 'invoice.xlsx'), index=False)
cm_df.to_excel(os.path.join(base, 'credit_memo.xlsx'), index=False)
concatenated_df.to_excel(os.path.join(base, 'concatenated.xlsx'), index=False)
# vat_df.to_excel(os.path.join(base, 'vat_reconciliation.xlsx'), index=False)
vat_df.sort_values(by='Posting Date GS', ascending=True).to_excel(os.path.join(base, 'vat_reconciliation.xlsx'), index=False)
# print(inv_df.info())
# print(cm_df.info())
# print(concatenated_df.info())
# print(vat_df.info())