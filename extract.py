"""Extract stage: pull the top coins by market cap from the CoinGecko API.

Writes a flat `top_coins.csv` that the transform stage picks up. The HTTP call
is wrapped with a timeout and automatic retries because the CoinGecko free tier
rate-limits aggressively (HTTP 429).
"""
import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry
import pandas as pd

API_URL = "https://api.coingecko.com/api/v3/coins/markets"

# Columns we keep from the (much wider) API response.
COLUMNS = [
    "id",
    "symbol",
    "name",
    "current_price",
    "market_cap",
    "total_volume",
    "price_change_percentage_24h",
    "price_change_percentage_7d_in_currency",
    "last_updated",
]


def _session() -> requests.Session:
    """A requests session that retries on rate-limit / transient 5xx errors."""
    retry = Retry(
        total=4,
        backoff_factor=2,  # waits 2s, 4s, 8s, 16s between attempts
        status_forcelist=(429, 500, 502, 503, 504),
        allowed_methods=("GET",),
    )
    session = requests.Session()
    session.mount("https://", HTTPAdapter(max_retries=retry))
    return session


def extract_top_coins(vs_currency="usd", per_page=100, page=1, timeout=30) -> pd.DataFrame:
    """Fetch the top `per_page` coins by market cap and return a flat DataFrame."""
    params = {
        "vs_currency": vs_currency,
        "order": "market_cap_desc",
        "per_page": per_page,
        "page": page,
        "price_change_percentage": "24h,7d",
    }

    response = _session().get(API_URL, params=params, timeout=timeout)
    response.raise_for_status()

    df = pd.json_normalize(response.json())

    missing = set(COLUMNS) - set(df.columns)
    if missing:
        raise ValueError(f"API response is missing expected columns: {sorted(missing)}")

    return df[COLUMNS]


if __name__ == "__main__":
    coins = extract_top_coins()
    coins.to_csv("top_coins.csv", index=False)
    print(f"Extracted {len(coins)} coins -> top_coins.csv")
