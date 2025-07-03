# src/data/csv_to_sqlite.py
import os
import pandas as pd
import sqlite3

def csv_to_sqlite(csv_dir: str, db_path: str):
    """
    Converts patient CSVs in a directory to a single SQLite database.
    Each CSV becomes a separate table.
    """
    if not os.path.exists(csv_dir):
        raise FileNotFoundError(f"Directory not found: {csv_dir}")

    conn = sqlite3.connect(db_path)
    print(f"Creating SQLite DB at {db_path} from CSVs in {csv_dir}")

    for file in os.listdir(csv_dir):
        if file.endswith(".csv"):
            table_name = os.path.splitext(file)[0].lower().replace(" ", "_")
            df = pd.read_csv(os.path.join(csv_dir, file))
            df.columns = [col.strip().lower().replace(" ", "_") for col in df.columns]
            df.to_sql(table_name, conn, if_exists="replace", index=False)
            print(f"Inserted table: {table_name} ({len(df)} rows)")

    conn.close()
    print("Patient data ingestion complete.")
