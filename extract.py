import pyodbc 
from dotenv import load_dotenv
import os
import pandas as pd

load_dotenv()

def get_connection(prefix):
    gs_server = os.getenv(f"{prefix}_SERVER")
    gs_database = os.getenv(f"{prefix}_DB")

    conn = pyodbc.connect(
        f'DRIVER={{ODBC Driver 17 for SQL Server}};'
        f'SERVER={gs_server};'
        f'DATABASE={gs_database};'
        f'Trusted_Connection=yes;'
        )
    return conn

conn = get_connection("GS") 
print(conn)

raw_data = pd.read_sql_query("SELECT * FROM [dbo].[gs_sales_invoice]", conn)


# df = pd.DataFrame()
print(raw_data.head())
print(raw_data.info())