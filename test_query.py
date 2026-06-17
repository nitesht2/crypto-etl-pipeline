"""Sanity check: print the 5 most recent rows from fact_coin_price."""
import pandas as pd

from db import get_engine


def main() -> None:
    engine = get_engine()
    df = pd.read_sql(
        "SELECT * FROM fact_coin_price ORDER BY last_updated DESC LIMIT 5;",
        engine,
    )
    print("Top 5 most recent rows from fact_coin_price:")
    print(df.to_string(index=False))


if __name__ == "__main__":
    main()
