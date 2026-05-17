import logging
from extract import extract_data 
import pandas as pd
from mappings import Mappings


def merge_documents(gs_df, pn_df, doc_type):
    # Merge GS and PN DataFrames based on document type (invoice or credit memo)

    logging.info(f"Merging {doc_type} documents from entities")

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
    logging.info(f"{doc_type.capitalize()} merge complete: {len(merged_df)} rows")
    return merged_df


def cm_amount_to_negative(cm_df):
    # Convert credit memo amounts to negative for reconciliation

    for column in Mappings.CM.keys():
        if column in cm_df.columns:
            cm_df[column] = cm_df[column] * -1

    return cm_df


def vat_reconciliation(inv_df, cm_df):
    # Rename columns and create a unified set of columns for both DataFrames
    logging.info("Performing VAT reconciliation")

    inv_df = inv_df.rename(columns=Mappings.VAT)
    cm_df = cm_df.rename(columns=Mappings.VAT)

    vat_columns = []
    for column in Mappings.VAT.values():
        if column in inv_df.columns or column in cm_df.columns:
            if column not in vat_columns:
                vat_columns.append(column)

    if "_merge" in inv_df.columns or "_merge" in cm_df.columns:
        vat_columns.append("_merge")

    inv_df = inv_df.reindex(columns=vat_columns)
    cm_df = cm_df.reindex(columns=vat_columns)

    vat_df = pd.concat([inv_df, cm_df], ignore_index=True)

    # Calculate VAT differences and control flags
    vat_df['Difference in Amount'] = vat_df['Amount GS'] - vat_df['Amount PN']
    vat_df['VAT Amount PN'] = vat_df['Amount Including VAT PN'] - vat_df['Amount PN']
    same_doc = vat_df["Document No. GS"] == vat_df["Order No. PN"]
    same_amount = vat_df["Amount GS"] == vat_df["Amount PN"]

    vat_df["Control"] = "Import"
    vat_df.loc[same_doc & same_amount, "Control"] = "Match"
    vat_df.loc[same_doc & ~same_amount, "Control"] = "Mismatch"

    logging.info(f"VAT reconciliation complete: {len(vat_df)} rows")
    return vat_df.sort_values(by=['Posting Date GS', 'Order No. GS'], ascending=True)


def import_orders(inv_df, cm_df, vat_df):
    # Rename columns and create a unified set of columns for both DataFrames
    logging.info("Preparing import orders")

    inv_df = inv_df.rename(columns=Mappings.IMPORT)
    cm_df = cm_df.rename(columns=Mappings.IMPORT)

    import_columns = []
    for column in Mappings.IMPORT.values():
        if column in inv_df.columns or column in cm_df.columns:
            if column not in import_columns:
                import_columns.append(column)

    inv_df = inv_df.reindex(columns=import_columns)
    cm_df = cm_df.reindex(columns=import_columns)

    import_df = pd.concat([inv_df, cm_df], ignore_index=True)

    # Find documents for import in PN
    import_orders = vat_df.loc[vat_df["_merge"] == "left_only", ["Document No. GS"]].drop_duplicates()

    # Filter import_df by matching keys
    import_df = import_df.merge(import_orders, on=["Document No. GS"], how="inner")
    
    logging.info(f"Import orders complete: {len(import_df)} records")
    return import_df


def transform_data():
    # Transformation pipeline
    logging.info("Starting data transformation")
    
    # Extract data using the extract module
    raw_dfs = extract_data()
    logging.info("Raw data extraction complete")

    # Merge invoices and credit memos from both company codes
    # logging.info("Merging invoice and credit memo documents")
    inv_df = merge_documents(raw_dfs['gs_inv'], raw_dfs['pn_inv'], 'invoice')
    cm_df = merge_documents(raw_dfs['gs_cm'], raw_dfs['pn_cm'], 'credit_memo')
    
    # Convert credit memo amounts to negative for reconciliation
    cm_df = cm_amount_to_negative(cm_df)

    # Perform VAT reconciliation
    vat_df = vat_reconciliation(inv_df, cm_df)

    # Perform import order
    import_df = import_orders(inv_df, cm_df, vat_df)

    logging.info("Data transformation complete")
    return inv_df, cm_df, vat_df, import_df