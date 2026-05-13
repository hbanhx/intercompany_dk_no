import pandas as pd
import pyodbc 
from dotenv import load_dotenv
import os

load_dotenv()

server = os.getenv("GS_SERVER")
database = os.getenv("GS_DB")


print(server)
conn = pyodbc.connect('DRIVER={ODBC Driver 17 for SQL Server};SERVER='+server+';DATABASE='+database+';Trusted_Connection=yes;')

print(conn)
cursor = conn.cursor()
cursor.execute("""SELECT TOP (1000) [Bill-to Customer No_]
      ,[Currency Code]
      ,[External Document No_]
      ,[No_]
      ,[Order Date]
      ,[Posting Date]
      ,[Sell-to Customer No_]
      ,[Ship-to Name]
      ,[Your Reference]
      ,[Ship-to Address]
      ,[Ship-to Address 2]
      ,[Ship-to City]
      ,[Ship-to Contact]
      ,[Ship-to Country_Region Code]
      ,[Ship-to County]
      ,[Ship-to Post Code]
      ,[Ship-to Code]
      ,[Ship-to Name 2]
      ,[Sales Invoice Line#Document No_]
      ,[Sales Invoice Line#Line No_]
      ,[Sales Invoice Line#No_]
      ,[Sales Invoice Line#Description]
      ,[Sales Invoice Line#Quantity]
      ,[Sales Invoice Line#Amount]
      ,[Sales Invoice Line#Amount Including VAT]
      ,[Sell-to Customer Name]
      ,[Sales Invoice Line#Unit Price]
      ,[Order No_]
      ,[Sell-to Contact]
  FROM [GS_DB].[dbo].['Sales Invoices GS$']""")
rows = cursor.fetchall()

for row in rows:
    print(row)


# db = pd.read_sql_query('SELECT TOP (1000) [Bill-to Customer No_], [Currency Code], [External Document No_], [No_], [Order Date], [Posting Date], [Sell-to Customer No_], [Ship-to Name], [Your Reference], [Ship-to Address], [Ship-to Address 2], [Ship-to City], [Ship-to Contact], [Ship-to Country_Region Code], [Ship-to County], [Ship-to Post Code], [Ship-to Code], [Ship-to Name 2] FROM [GS_DB].[dbo].["Sales Invoices GS$"]', conn)
# print(db)