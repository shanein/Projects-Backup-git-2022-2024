import pandas as pd

data = pd.read_csv("Liquor_Sales.csv", dtype={"Item Number": "str"}, low_memory=False)
print(type(data))
print(data.shape)

import duckdb as ddb
con = ddb.connect("my-working-database.db")
# con.sql("""create table liquor as (select * from data)""")
result = con.execute("select * from liquor")
rows = result.fetchall()

con.close()

for row in rows:
   print(row)

# from operator import add
