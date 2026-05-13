import pandas as pd
import pyodbc 
from dotenv import load_dotenv
import os

load_dotenv()

server = os.getenv("GS_SERVER")
database = os.getenv("GS_DB")


print(server)
conn = pyodbc.connect('DRIVER={ODBC Driver 17 for SQL Server};SERVER='+server+';DATABASE='+database+';Trusted_Connection=yes;')