import extract 
import os
import pandas as pd
import numpy as np
# import openpyxl


def vat_columns_mapping():
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


def import_columns_mapping():
    mapping = {
        # GS invoice header
        "invoice_gs_doc_type": "Document Type",        
        "invoice_gs_No_": "Document No.",
        "invoice_gs_Sell-to Customer No_": "Customer No.",        
        "invoice_gs_Your Reference": "Reference",
        "invoice_gs_Ship-to Name": "Ship-to Name",
        "invoice_gs_Ship-to Name 2": "Ship-to Name 2",
        "invoice_gs_Ship-to Address": "Ship-to Address",
        "invoice_gs_Ship-to Address 2": "Ship-to Address 2",
        "invoice_gs_Ship-to City": "Ship-to City",
        "invoice_gs_Ship-to Contact": "Ship-to Contact",
        "invoice_gs_Order Date": "Order Date",
        "invoice_gs_Posting Date": "Posting Date",
        "invoice_gs_Sell-to Contact": "Contact Name",
        "invoice_gs_Ship-to Post Code": "Ship-to Post Code",     
        "invoice_gs_Ship-to County": "Ship-to County",
        "invoice_gs_Ship-to Country_Region Code": "Ship-to Country Region Code",
        "invoice_gs_External Document No_": "External Document No.",

        # GS credit memo header
        "credit_memo_gs_doc_type": "Document Type",        
        "credit_memo_gs_No_": "Document No.",
        "credit_memo_gs_Sell-to Customer No_": "Customer No.",        
        "credit_memo_gs_Your Reference": "Reference",
        "credit_memo_gs_Ship-to Name": "Ship-to Name",
        "credit_memo_gs_Ship-to Name 2": "Ship-to Name 2",
        "credit_memo_gs_Ship-to Address": "Ship-to Address",
        "credit_memo_gs_Ship-to Address 2": "Ship-to Address 2",
        "credit_memo_gs_Ship-to City": "Ship-to City",
        "credit_memo_gs_Ship-to Contact": "Ship-to Contact",
        "credit_memo_gs_Order Date": "Order Date",
        "credit_memo_gs_Posting Date": "Posting Date",
        "credit_memo_gs_Sell-to Contact": "Contact Name",
        "credit_memo_gs_Ship-to Post Code": "Ship-to Post Code",     
        "credit_memo_gs_Ship-to County": "Ship-to County",
        "credit_memo_gs_Ship-to Country_Region Code": "Ship-to Country Region Code",
        "credit_memo_gs_External Document No_": "External Document No.",

        # GS invoice lines
        "invoice_gs_Sales Invoice Line#Line No_": "Line No.",
        "invoice_gs_Type": "Item",
        "invoice_gs_Sales Invoice Line#No_": "Item No.",
        "invoice_gs_Sales Invoice Line#Quantity": "Quantity",
        "invoice_gs_Sales Invoice Line#Unit Price": "Unit Price",

        # GS credit memo lines
        "credit_memo_gs_No_": "No.",
        "credit_memo_gs_Sales Cr_Memo Line#Line No_": "Line No.",
        "credit_memo_gs_Type": "Item",
        "credit_memo_gs_Sales Cr_Memo Line#No_": "Item No.",
        "credit_memo_gs_Sales Cr_Memo Line#Quantity": "Quantity",
        "credit_memo_gs_Sales Cr_Memo Line#Unit Price": "Unit Price",

    }
    return mapping

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
    # Rename columns and create a unified set of columns for both DataFrames
    df1 = df1.rename(columns=vat_columns_mapping())
    df2 = df2.rename(columns=vat_columns_mapping())

    vat_columns = []
    for col in vat_columns_mapping().values():
        if col in df1.columns or col in df2.columns:
            if col not in vat_columns:
                vat_columns.append(col)

    if "_merge" in df1.columns or "_merge" in df2.columns:
        vat_columns.append("_merge")

    df1 = df1.reindex(columns=vat_columns)
    df2 = df2.reindex(columns=vat_columns)

    vat_df = pd.concat([df1, df2], ignore_index=True)

    # Calculate VAT differences and control flags
    vat_df['Difference in Amount'] = vat_df['Amount GS'] - vat_df['Amount PN']
    vat_df['VAT Amount PN'] = vat_df['Amount Including VAT PN'] - vat_df['Amount PN']
    vat_df["Control"] = np.where(
            vat_df["Document No. GS"] == vat_df["Order No. PN"],
            np.where(
                vat_df["Amount GS"] == vat_df["Amount PN"],
            "Match",
            "Mismatch"
        ),
        "Import"
    )

    return vat_df.sort_values(by=['Posting Date GS', 'Order No. GS'], ascending=True)

def import_orders(df1, df2, mask):
    # Rename columns and create a unified set of columns for both DataFrames
    df1 = df1.rename(columns=import_columns_mapping())
    df2 = df2.rename(columns=import_columns_mapping())

    import_columns = []
    for col in import_columns_mapping().values():
        if col in df1.columns or col in df2.columns:
            if col not in import_columns:
                import_columns.append(col)

    df1 = df1.reindex(columns=import_columns)
    df2 = df2.reindex(columns=import_columns)

    import_df = pd.concat([df1, df2], ignore_index=True)
    import_df = import_df[mask]

    return import_df


def transform_data():
    # Transformation pipeline

    # Extract data using the extract module
    raw_dfs = extract.extract_data()

    # Merge invoices and credit memos from both company codes
    inv_df = merge_documents(raw_dfs['gs_inv'], raw_dfs['pn_inv'], 'invoice')
    cm_df = merge_documents(raw_dfs['gs_cm'], raw_dfs['pn_cm'], 'credit_memo')

    # Convert credit memo amounts to negative for reconciliation
    cm_df = cm_df[["credit_memo_gs_Sales Cr_Memo Line#Amount", 
                   "credit_memo_gs_Sales Cr_Memo Line#Amount Including VAT", 
                   "credit_memo_gs_Sales Cr_Memo Line#Unit Price",
                   "credit_memo_pn_Sales Cr_Memo Line#Amount", 
                   "credit_memo_pn_Sales Cr_Memo Line#Amount Including VAT", 
                   "credit_memo_pn_Sales Cr_Memo Line#Unit Price"]] * -1

    # Concatenate the merged DataFrames to create a unified dataset
    concatenated_df = concatenate_dataframes(inv_df, cm_df)

    # Perform VAT reconciliation
    vat_df = vat_reconciliation(df1=inv_df, df2=cm_df)

    # Perform import order
    # gs_inv_df = raw_dfs['gs_inv'].add_prefix("invoice_gs_")
    # gs_cm_df = raw_dfs['gs_cm'].add_prefix("credit_memo_gs_")
    mask_pn_import = vat_df['_merge'] == 'left_only'
    print(type(mask_pn_import))
    import_df = import_orders(df1=inv_df, df2=cm_df, mask=mask_pn_import)


    return inv_df, cm_df, concatenated_df, vat_df, import_df



inv_df, cm_df, concatenated_df, vat_df, import_df = transform_data()

base = os.path.dirname(os.path.abspath(__file__))
inv_df.to_excel(os.path.join(base, 'invoice.xlsx'), index=False)
cm_df.to_excel(os.path.join(base, 'credit_memo.xlsx'), index=False)
concatenated_df.to_excel(os.path.join(base, 'concatenated.xlsx'), index=False)
# vat_df.to_excel(os.path.join(base, 'vat_reconciliation.xlsx'), index=False)
vat_df.sort_values(by='Posting Date GS', ascending=True).to_excel(os.path.join(base, 'vat_reconciliation.xlsx'), index=False)
import_df.to_excel(os.path.join(base, 'import_orders.xlsx'), index=False)
# print(inv_df.info())
# print(cm_df.info())
# print(concatenated_df.info())
# print(vat_df.info())
# print(import_df.info())