"""Load stage: append the transformed CSV into the PostgreSQL fact table.

Credentials come from the environment via db.get_engine() — never hard-coded.
Append mode builds a time series: one row per coin per run.
"""
import pandas as pd

from db import get_engine


def load_data(input_file="top_coins_transformed.csv", table_name="fact_coin_price") -> int:
    df = pd.read_csv(input_file)

    engine = get_engine()
    df.to_sql(name=table_name, con=engine, if_exists="append", index=False)

    print(f"Loaded {len(df)} rows into PostgreSQL table '{table_name}'")
    return len(df)


if __name__ == "__main__":
    load_data()
