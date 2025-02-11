import pandas as pd
from sqlalchemy import create_engine

# Database connection
DB_TYPE = "sqlite"
DB_NAME = "urls_database.db"
TABLE_NAME = "urls"

if DB_TYPE == "sqlite":
    engine = create_engine(f"sqlite:///{DB_NAME}")
elif DB_TYPE == "postgresql":
    engine = create_engine("postgresql://username:password@localhost:5432/your_db_name")

# Load CSV into the database
csv_file = "2024-05-17-mängelmelder_urls.csv"  # Ensure this file exists
df = pd.read_csv(csv_file, encoding='latin1')

# Debug: Print column names
print("CSV Column Names:", df.columns.tolist())

# Ensure 'url' column exists
if "url" not in df.columns:
    raise ValueError(f"Error: No 'url' column found. Available columns: {df.columns.tolist()}")

# Save to database
df.to_sql(TABLE_NAME, con=engine, if_exists="replace", index=False)
print("✅ CSV successfully loaded into the database!")

