import json
import csv
import os

DATA_DIR = "data"
USERS_FILE = os.path.join(DATA_DIR, "users.json")
ACCOUNTS_FILE = os.path.join(DATA_DIR, "accounts.json")
TRANSACTIONS_FILE = os.path.join(DATA_DIR, "transactions.csv")

def load_data():
    # Load users
    if os.path.exists(USERS_FILE):
        with open(USERS_FILE, "r") as f:
            users = json.load(f)
    else:
        users = {}

    # Load accounts
    if os.path.exists(ACCOUNTS_FILE):
        with open(ACCOUNTS_FILE, "r") as f:
            accounts = json.load(f)
    else:
        accounts = {}

    # Load transactions
    transactions = []
    if os.path.exists(TRANSACTIONS_FILE):
        with open(TRANSACTIONS_FILE, newline='') as f:
            reader = csv.DictReader(f)
            for row in reader:
                row["amount"] = float(row["amount"])
                transactions.append(row)

    return users, accounts, transactions

def save_data(users, accounts, transactions):
    os.makedirs(DATA_DIR, exist_ok=True)

    with open(USERS_FILE, "w") as f:
        json.dump(users, f, indent=4)

    with open(ACCOUNTS_FILE, "w") as f:
        json.dump(accounts, f, indent=4)

    with open(TRANSACTIONS_FILE, "w", newline='') as f:
        fieldnames = ["account_id", "type", "amount", "description", "timestamp"]
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        for tx in transactions:
            writer.writerow(tx)
