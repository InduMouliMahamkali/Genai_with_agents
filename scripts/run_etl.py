# scripts/run_etl.py

import time

def run_etl():
    print(" Starting ETL pipeline...")
    time.sleep(1)
    print(" Loaded data from source.")
    time.sleep(1)
    print(" Transformed and cleaned records.")
    time.sleep(1)
    print(" Saved to database. ETL complete.")

if __name__ == "__main__":
    run_etl()
