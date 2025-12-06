from config.config import get_database

db = get_database()

table_name = "pioma_proj.apartments"

df= db.fetch_as_dataframe(table_name=table_name)

print(df)