import pandas as pd
import sqlite3

# Load the Excel file
file_path = "2024-05-17-mängelmelder_urls.xlsx"  # Ensure this is in the same directory
df = pd.read_excel(file_path)

# Check for missing values and clean data
df.dropna(inplace=True)

# Connect to SQLite database (creates a new file if it doesn't exist)
conn = sqlite3.connect("mangelmelder_urls.db")

# Save DataFrame to SQLite
df.to_sql("urls", conn, if_exists="replace", index=False)

# Close the connection
conn.close()

print("✅ Database created successfully!")
