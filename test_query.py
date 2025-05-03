import pandas as pd
from sqlalchemy import create_engine

db_user = "crypto_user"
db_pass = "***REMOVED***"
db_host = "localhost"
db_port = "5432"
db_name = "crypto_db"

engine = create_engine(f"postgresql+psycopg2://{db_user}:{db_pass}@{db_host}:{db_port}/{db_name}")
query = "SELECT * FROM fact_coin_price LIMIT 5;"
df = pd.read_sql(query, engine)

print("✅ Top 5 rows from fact_coin_price table:")
print(df)