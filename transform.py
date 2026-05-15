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


def merge_documents(gs_df, pn_df, doc_type):
    # 


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

def vat_reconciliation(df):
    # Ret
    columns = [column for column in columns_mapping().values() if column in df.columns]
    columns.append('_merge')  
    vat_df = df[columns]
    return vat_df



def transform_data():
    # Transformation pipeline

    # Extract data using the extract module
    raw_dfs = extract.extract_data()

    # Merge invoices and credit memos from both company codes
    inv_df = merge_documents(raw_dfs['gs_inv'], raw_dfs['pn_inv'], 'invoice')
    cm_df = merge_documents(raw_dfs['gs_cm'], raw_dfs['pn_cm'], 'credit_memo')

    # Rename columns for clarity
    inv_df = inv_df.rename(columns=columns_mapping())
    cm_df = cm_df.rename(columns=columns_mapping())

    # Select relevant columns for the final output (optional, can be adjusted based on requirements)

    # Concatenate the merged DataFrames to create a unified dataset
    concatenated_df = concatenate_dataframes(inv_df, cm_df)

    # Perform VAT reconciliation
    vat_df = vat_reconciliation(concatenated_df)

    # New intercompany transaction for posting


    return inv_df, cm_df, concatenated_df, vat_df


inv_df, cm_df, concatenated_df, vat_df = transform_data()

base = os.path.dirname(os.path.abspath(__file__))
inv_df.to_excel(os.path.join(base, 'invoice.xlsx'), index=False)
cm_df.to_excel(os.path.join(base, 'credit_memo.xlsx'), index=False)
concatenated_df.to_excel(os.path.join(base, 'concatenated.xlsx'), index=False)
vat_df.to_excel(os.path.join(base, 'vat_reconciliation.xlsx'), index=False)
print(inv_df.info())
print(cm_df.info())
print(concatenated_df.info())
print(vat_df.info())