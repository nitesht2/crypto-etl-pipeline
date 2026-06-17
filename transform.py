"""Transform stage: clean the extracted CSV and derive analytic fields.

- Parse `last_updated` to a real timestamp
- Round price / percentage fields for readability
- Rename the verbose 7d column to match the warehouse schema
- Derive `is_volatile_24h` (abs 24h change > 10%)
"""
import pandas as pd

VOLATILITY_THRESHOLD = 10.0  # percent


def transform_data(input_file="top_coins.csv", output_file="top_coins_transformed.csv") -> pd.DataFrame:
    df = pd.read_csv(input_file)

    df["last_updated"] = pd.to_datetime(df["last_updated"], errors="coerce")

    # Match the documented warehouse column name (fact_coin_price).
    df = df.rename(
        columns={"price_change_percentage_7d_in_currency": "price_change_percentage_7d"}
    )

    for col in ["current_price", "price_change_percentage_24h", "price_change_percentage_7d"]:
        df[col] = df[col].round(2)

    # NaN 24h change -> not volatile (fillna avoids NaN leaking into the flag).
    df["is_volatile_24h"] = df["price_change_percentage_24h"].abs().fillna(0) > VOLATILITY_THRESHOLD

    df.to_csv(output_file, index=False)
    print(f"Transformed {len(df)} rows -> {output_file}")
    return df


if __name__ == "__main__":
    transform_data()
