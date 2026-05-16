import pyodbc 
from dotenv import load_dotenv
import os
import pandas as pd


load_dotenv()

def get_connection(prefix):
    gs_driver = os.getenv(f"{prefix}_DRIVER")
    gs_server = os.getenv(f"{prefix}_SERVER")
    gs_database = os.getenv(f"{prefix}_DB")
    conn = pyodbc.connect(
        f'DRIVER={gs_driver};'
        f'SERVER={gs_server};'
        f'DATABASE={gs_database};'
        f'Trusted_Connection=yes;'
        )
    return conn

def create_df(connection_prefix, db):
    # Establish connection and execute query to create DataFrame
    conn = get_connection(connection_prefix)
    raw_df = pd.read_sql_query(db, conn)
    return raw_df       

def extract_data():
    # SQL statements for each table
    sql_gs_inv = "SELECT * FROM [dbo].[gs_sales_invoice] WHERE [Posting Date] >= '2025-03-01'"
    sql_gs_cm = "SELECT * FROM [dbo].[gs_sales_credit_memo] WHERE [Posting Date] >= '2025-03-01'"
    sql_pn_inv = "SELECT * FROM [dbo].[pn_sales_invoice] WHERE [Posting Date] >= '2025-03-01'"
    sql_pn_cm = "SELECT * FROM [dbo].[pn_sales_credit_memo] WHERE [Posting Date] >= '2025-03-01'"
    
    # Create DataFrames for each table and return as a dictionary
    return {
        'gs_inv': create_df('GS', sql_gs_inv),
        'gs_cm': create_df('GS', sql_gs_cm),
        'pn_inv': create_df('PN', sql_pn_inv),
        'pn_cm': create_df('PN', sql_pn_cm)
    }