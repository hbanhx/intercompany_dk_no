GS → PN Intercompany Invoice Synchronization & Reconciliation

This project contains a Python ETL pipeline that compares invoice and credit memo data between GS Denmark and PN Norway. It checks that the data sent from GS NAV to PN NAV is complete and correct for domestic invoicing and VAT reporting. All SQL tables used in this project are fake, and all sample data is fully masked.

Core Capabilities

    Line‑by‑line comparison of GS and PN invoice and credit memo data

    Finding missing or mismatched lines in PN

    Checking fields that affect VAT

    Creating PN posting files for documents that did not transfer

    Making GS and PN data follow the same structure using mapping rules

    Merging data using NAV keys (DocumentNo + LineNo)

    Running SQL queries through a simple config file

How It Works

    extract.py reads SQL queries from config.yaml and loads data from GS and PN

    transform.py merges invoices and credit memos, adjusts credit memo amounts, performs VAT checks, and finds missing PN documents

    load.py exports the final datasets to Excel files in the output folder

    mappings.py contains all column mapping rules for invoices, credit memos, VAT, and import orders

Why This Matters
    PN Norway sends invoices to Norwegian customers.
    GS Denmark ships the goods and posts the financial entry.
    Because of this setup, PN must receive correct data from GS to:

    Rebuild GS invoices in PN NAV

    Apply Norwegian VAT rules

    Send proper invoices to customers

    Keep financial data accurate

Designed For

    NAV/Business Central setups between two companies

    Automated invoice and credit memo flows

    VAT handling across countries

    Financial data checks

    Systems that send invoices automatically

Data Safety

    All data in this project is masked

    All SQL tables are fake

    No personal or company‑sensitive data is included