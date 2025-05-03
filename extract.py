# Import the requests library to make HTTP requests to the API
import requests
# Import pandas to work with tabular data (like DataFrames)
import pandas as pd

# Define a function to extract the top cryptocurrencies from the CoinGecko API
def extract_top_coins(vs_currency="usd", per_page=100, page=1):
    # Define the API endpoint URL
    url = "https://api.coingecko.com/api/v3/coins/markets"
    
    # Define the parameters we want to pass to the API
    params = {
        "vs_currency": vs_currency,               # Currency to show prices in (default: USD)
        "order": "market_cap_desc",               # Sort by market cap, descending
        "per_page": per_page,                     # Number of coins per page (max: 250)
        "page": page,                             # Page number (default: 1)
        "price_change_percentage": "24h,7d"      # Include % change over 24h and 7d
    }
    
    # Make the GET request to the API with parameters
    response = requests.get(url, params=params)
    
    # Check if the request was successful (HTTP 200 OK)
    if response.status_code == 200:
        # Parse the JSON response into a Python object
        data = response.json()
        
        # Use pandas to normalize the nested JSON into a flat DataFrame
        df = pd.json_normalize(data)
        
        # Select only the important columns we care about
        df = df[[
            'id',                                 # Coin ID (e.g., bitcoin)
            'symbol',                             # Symbol (e.g., BTC)
            'name',                               # Name (e.g., Bitcoin)
            'current_price',                      # Current price in USD
            'market_cap',                         # Market capitalization
            'total_volume',                       # Trading volume over 24h
            'price_change_percentage_24h',        # % price change over 24h
            'price_change_percentage_7d_in_currency',  # % price change over 7d
            'last_updated'                        # Timestamp of last update
        ]]
        
        # Return the DataFrame so we can use it later
        return df
    else:
        # If the API call failed, raise an exception with the error code
        raise Exception(f"API call failed with status code {response.status_code}")

# This block runs if we call the script directly (not when imported as a module)
if __name__ == "__main__":
    # Call the extract function and store the DataFrame
    df = extract_top_coins()
    
    # Print the first 5 rows so we can check the data in the terminal
    print(df.head())
    
    # Save the DataFrame as a CSV file called 'top_coins.csv' (no index column)
    df.to_csv("top_coins.csv", index=False)
    
    # Print a success message
    print("✅ Data extracted and saved to top_coins.csv")