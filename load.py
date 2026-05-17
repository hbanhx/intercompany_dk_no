import logging
import os


def load_data(inv_df, cm_df, vat_df, import_df):

    # Load data into Excel files
    base = os.path.dirname(os.path.abspath(__file__))
    output_dir = os.path.join(base, "output")
    os.makedirs(output_dir, exist_ok=True)

    inv_path    = os.path.join(output_dir, 'invoices.xlsx')
    cm_path     = os.path.join(output_dir, 'credit_memos.xlsx')
    vat_path    = os.path.join(output_dir, 'vat_reconciliation.xlsx')
    import_path = os.path.join(output_dir, 'import_orders.xlsx')

    inv_df.to_excel(inv_path, index=False)
    logging.info(f"Saved invoices file: {os.path.relpath(inv_path)}")

    cm_df.to_excel(cm_path, index=False)
    logging.info(f"Saved credit memos file: {os.path.relpath(cm_path)}")

    vat_df.sort_values(by='Posting Date GS', ascending=True).to_excel(vat_path, index=False)
    logging.info(f"Saved VAT reconciliation file: {os.path.relpath(vat_path)}")
    
    import_df.to_excel(import_path, index=False)
    logging.info(f"Saved import orders file: {os.path.relpath(import_path)}")

    logging.info("Data loaded into Excel files successfully")