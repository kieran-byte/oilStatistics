import pandas as pd
import sqlite3
import csv


# Function to create the table for oil prices
def create_daily_oil_price_table():
    conn = sqlite3.connect('oil_prices.db')  # Connecting to SQLite database (or create if doesn't exist)
    cursor = conn.cursor()

    # Create a table named 'OilPrices' with columns 'Date' and 'Price'
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS YearlyOilPrice (
            Date DATE PRIMARY KEY,
            Price DECIMAL(18, 2),
            PriceChange DECIMAL(18, 2)
        )
    ''')

    # Create a table named 'OilPrices' with columns 'Date' and 'Price'
    cursor.execute('''
            CREATE TABLE IF NOT EXISTS YearlyOilProd (
                Date DATE PRIMARY KEY,
                Prod DECIMAL(18, 2),
                ProdChange DECIMAL(18, 2)
            )
        ''')

    conn.commit()
    conn.close()


# Function to insert oil price data into the table
def insert_oil_prod(date, prod, Change):
    conn = sqlite3.connect('oil_prices.db')
    cursor = conn.cursor()

    # Insert data into 'OilPrices' table
    cursor.execute('''
        INSERT INTO YearlyOilProd (Date, Prod, ProdChange)
        VALUES (?, ?, ?)
    ''', (date, prod, Change))

    conn.commit()
    conn.close()


# Function to insert oil price data into the table
def insert_oil_price(date, price, Change):
    conn = sqlite3.connect('oil_prices.db')
    cursor = conn.cursor()

    # Insert data into 'OilPrices' table
    cursor.execute('''
        INSERT INTO YearlyOilPrice (Date, Price, PriceChange)
        VALUES (?, ?, ?)
    ''', (date, price, Change))

    conn.commit()
    conn.close()


conn = sqlite3.connect('oil_prices.db')
cursor = conn.cursor()

sql = "DROP TABLE IF EXISTS YearlyOilPrice"
cursor.execute(sql)
sql = "DROP TABLE IF EXISTS YearlyOilProd"
cursor.execute(sql)
create_daily_oil_price_table()

csv_file = 'data/brent-year.csv'

with open(csv_file, newline='') as file:
    reader = csv.reader(file)
    header = next(reader)  # Get the header row

    # Get initial price for calculation
    old_price = next(reader)[1]  # Get the first row after the header

    # Iterate through the remaining rows to calculate changes and insert data
    for row in reader:
        date = row[0].split('-')[0]  # Extracting year from the date
        price = row[1]

        try:
            price_change = ((float(price) - float(old_price)) / float(old_price)) * 100
            price_change = round(price_change, 2)

            # Call function to insert data into the database
            insert_oil_price(date, price, price_change)

            # Update old price for the next iteration
            old_price = price
        except ValueError:
            # Handle the case where conversion to float fails
            print(f"Error: Non-numeric data found in row with date: {date}")

csv_file = 'data/oilProd.csv'

with open(csv_file, newline='') as file:
    reader = csv.reader(file)
    header = next(reader)  # header row

    # Initialize variables for tracking changes
    old_prod_values = [float(value) for value in next(reader)[1:]]  # Get the first row after the header
    old_prod_sum = sum(old_prod_values)

    # Iterate through the remaining rows to calculate changes and insert data
    for row in reader:
        date = row[0]
        try:
            prod_values = [float(value) for value in row[1:]]  # Convert values to floats
            prod_sum = sum(prod_values)

            # Calculate percentage change in oil production
            prod_change = ((prod_sum - old_prod_sum) / old_prod_sum) * 100
            prod_change = round(prod_change, 2)

            # Call function to insert data into the database
            insert_oil_prod(date, prod_sum, prod_change)

            # Update old values for the next iteration
            old_prod_sum = prod_sum
        except ValueError:
            # Handle the case where conversion to float fails
            print(f"Error: Non-numeric data found in row with date: {date}")


# All data is now in the database, check if their is a statistical correlation between the two
conn = sqlite3.connect('oil_prices.db')

# Fetch data from SQL tables into Pandas DataFrames
oil_production_df = pd.read_sql_query("SELECT * FROM YearlyOilProd", conn)
oil_price_df = pd.read_sql_query("SELECT * FROM YearlyOilPrice", conn)

conn.close()

# Merge the two DataFrames on 'Year'
merged_df = pd.merge(oil_production_df, oil_price_df, on='Date', how='inner')

# Calculate the correlation coefficient between the two variables
correlation_coefficient = merged_df['ProdChange'].corr(merged_df['PriceChange'])

print(f"Correlation Coefficient: {correlation_coefficient}")
