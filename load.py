import pandas as pd
from sqlalchemy import create_engine

def load_data(
    input_file="top_coins_transformed.csv",
    db_user="crypto_user",
    db_pass="***REMOVED***",  # ← replace with the password you set in psql
    db_host="localhost",
    db_port="5432",
    db_name="crypto_db",
    table_name="fact_coin_price"
):
    # Read the transformed CSV
    df = pd.read_csv(input_file)

    # Build the connection string for PostgreSQL
    conn_str = f"postgresql+psycopg2://{db_user}:{db_pass}@{db_host}:{db_port}/{db_name}"

    # Create the SQLAlchemy engine
    engine = create_engine(conn_str)

    # Load data into the table (append mode)
    df.to_sql(
        name=table_name,
        con=engine,
        if_exists='append',  # use 'replace' if you want to wipe the table each time
        index=False
    )

    print(f"✅ Data loaded into PostgreSQL table '{table_name}'")

if __name__ == "__main__":
    load_data()