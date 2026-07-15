import os
import sys
from sqlalchemy import create_engine, inspect, text

# Append parent directory to sys.path so we can import etl and transform
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from etl import build_fact_table
from transform import engineer_leakage_features

def load_to_db(df, table_name="fact_orders_leakage"):
    """Loads the fact table dataframe to MySQL, falling back to SQLite on connection failure."""
    # We allow overrides via environment variables or default to standard connection string
    mysql_uri = os.environ.get("MYSQL_DB_URI", "mysql+pymysql://user:password@localhost:3306/olist_leakage_db")

    def _write_table(engine):
        inspector = inspect(engine)
        if not inspector.has_table(table_name):
            # Create an empty table with the dataframe schema first, then append data.
            df.head(0).to_sql(table_name, con=engine, if_exists="replace", index=False)
        else:
            # Clear existing rows without dropping indexes or rebuilding the table.
            with engine.begin() as conn:
                conn.execute(text(f"DELETE FROM {table_name}"))

        df.to_sql(table_name, con=engine, if_exists="append", index=False, chunksize=5000, method="multi")

    try:
        print(f"Connecting to MySQL: {mysql_uri.split('@')[-1]}")
        engine = create_engine(mysql_uri, connect_args={"connect_timeout": 3})
        # Test connection quickly
        with engine.connect() as conn:
            pass

        # Write to MySQL
        _write_table(engine)
        print(f"Successfully loaded {len(df)} rows into MySQL table: {table_name}")
        return True
    except Exception as e:
        print(f"\n[WARNING] MySQL loading failed: {e}")
        print("Attempting SQLite fallback...")
        
        try:
            # Setup path to SQLite db
            db_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "data")
            os.makedirs(db_dir, exist_ok=True)
            sqlite_path = os.path.abspath(os.path.join(db_dir, "olist_leakage_db.db"))
            sqlite_uri = f"sqlite:///{sqlite_path}"
            
            engine = create_engine(sqlite_uri)
            _write_table(engine)
            print(f"Successfully loaded {len(df)} rows into SQLite table '{table_name}' at: {sqlite_path}")
            return True
        except Exception as sqlite_error:
            print(f"[ERROR] SQLite loading failed: {sqlite_error}")
            return False

if __name__ == "__main__":
    project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
    data_dir = os.path.join(project_root, "data")
    
    print("Starting ETL + Feature Engineering + Database Load Pipeline...")
    
    # 1. Run ETL to build fact table
    print("Step 1: Extracting raw CSV files & building fact table...")
    df = build_fact_table(data_dir)
    
    # 2. Run Transform to engineer features
    print("Step 2: Engineering leakage features and labels...")
    df = engineer_leakage_features(df)
    
    # 3. Save to local CSV for easy notebook and Streamlit consumption
    csv_out_path = os.path.join(data_dir, "processed_fact_orders.csv")
    print(f"Step 3: Exporting processed file to {csv_out_path}...")
    df.to_csv(csv_out_path, index=False)
    
    # 4. Load to Database
    print("Step 4: Loading data to SQL Warehouse...")
    load_to_db(df)
    
    print("Pipeline Execution Completed.")
