import logging
import os


def load_data(inv_df, cm_df, vat_df, import_df):

    # Load the transformed DataFrames into Excel files
    base = os.path.dirname(os.path.abspath(__file__))
    inv_df.to_excel(os.path.join(base, 'invoice.xlsx'), index=False)
    cm_df.to_excel(os.path.join(base, 'credit_memo.xlsx'), index=False)
    vat_df.sort_values(by='Posting Date GS', ascending=True).to_excel(os.path.join(base, 'vat_reconciliation.xlsx'), index=False)
    import_df.to_excel(os.path.join(base, 'import_orders.xlsx'), index=False)
    logging.info("Data loaded into Excel files successfully")
