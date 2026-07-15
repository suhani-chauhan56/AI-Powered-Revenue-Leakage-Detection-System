import os
import sys

import sqlalchemy
from sqlalchemy import text


def main():
    mysql_uri = os.environ.get("MYSQL_DB_URI")
    if not mysql_uri:
        print("MYSQL_DB_URI is not set. Skipping the MySQL connection test.")
        print("Set MYSQL_DB_URI to validate a real database connection.")
        return 0

    print(f"Testing MySQL connection: {mysql_uri.split('@')[-1]}")
    try:
        engine = sqlalchemy.create_engine(mysql_uri, connect_args={"connect_timeout": 3})
        with engine.connect() as conn:
            conn.execute(text("SELECT 1"))
        print("SUCCESS: MySQL connection is working.")
        return 0
    except Exception as e:
        print(f"FAILED: {e}")
        print("Set MYSQL_DB_URI to a valid connection string and make sure the database exists.")
        return 1


if __name__ == "__main__":
    sys.exit(main())
