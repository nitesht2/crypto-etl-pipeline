# Import pandas library to work with tabular data
import pandas as pd

# Define a function to transform the data
def transform_data(input_file="top_coins.csv", output_file="top_coins_transformed.csv"):
    # Load the extracted data from the CSV file into a DataFrame
    df = pd.read_csv(input_file)

    # Convert 'last_updated' column from string to datetime format
    df['last_updated'] = pd.to_datetime(df['last_updated'])

    # Round numeric columns to 2 decimal places for better readability and consistency
    df['current_price'] = df['current_price'].round(2)
    df['price_change_percentage_24h'] = df['price_change_percentage_24h'].round(2)
    df['price_change_percentage_7d_in_currency'] = df['price_change_percentage_7d_in_currency'].round(2)

    # Add a new column: 'is_volatile_24h'
    # Mark as True if the absolute value of the 24h price change is greater than 10%
    df['is_volatile_24h'] = df['price_change_percentage_24h'].abs() > 10

    # Save the transformed DataFrame to a new CSV file
    df.to_csv(output_file, index=False)

    # Print a success message to the console
    print(f"✅ Data transformed and saved to {output_file}")

# This block runs if the script is executed directly (not imported as a module)
if __name__ == "__main__":
    transform_data()