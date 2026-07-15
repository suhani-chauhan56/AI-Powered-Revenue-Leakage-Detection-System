import sqlalchemy
import sys

passwords = ["", "root", "admin", "password", "1234", "123456", "mysql", "12345678"]
found = False

for pwd in passwords:
    if pwd == "":
        uri = "mysql+pymysql://root@localhost:3306"
        desc = "no password"
    else:
        uri = f"mysql+pymysql://root:{pwd}@localhost:3306"
        desc = f"password '{pwd}'"
        
    try:
        engine = sqlalchemy.create_engine(uri, connect_args={"connect_timeout": 1})
        with engine.connect() as conn:
            print(f"SUCCESS: Connected to MySQL as root with {desc}!")
            print(f"Use connection string: {uri}/olist_leakage_db")
            found = True
            break
    except Exception as e:
        # Check if the error is due to database not existing vs access denied
        err_msg = str(e)
        if "1049" in err_msg or "Unknown database" in err_msg:
            # 1049 means credentials are correct, but the db doesn't exist yet, which is a success!
            print(f"SUCCESS (DB doesn't exist yet but credentials are correct): root with {desc}")
            print(f"Use connection string: {uri}/olist_leakage_db")
            found = True
            break
        elif "1045" in err_msg or "Access denied" in err_msg:
            # Wrong password
            pass
        else:
            print(f"Other connection error with {desc}: {err_msg}")

if not found:
    print("FAILED: Could not connect to MySQL with any common root passwords. Please make sure MySQL is running and you have the correct password.")
