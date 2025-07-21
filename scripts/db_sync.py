# scripts/db_sync.py

import time

def sync_database():
    print(" Connecting to DB...")
    time.sleep(1)
    print("Syncing tables: users, transactions, metrics...")
    time.sleep(1)
    print(" Database sync complete.")

if __name__ == "__main__":
    sync_database()
