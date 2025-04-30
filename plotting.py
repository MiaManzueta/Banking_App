import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime

def plot_balance_trend(transactions, account_id):
    # Filter transactions for the given account
    filtered = [tx for tx in transactions if tx["account_id"] == account_id]
    if not filtered:
        print("No transactions available for this account.")
        return

    # Create DataFrame
    df = pd.DataFrame(filtered)
    df["timestamp"] = pd.to_datetime(df["timestamp"])
    df.sort_values("timestamp", inplace=True)

    # Calculate running balance
    balance = 0
    balances = []
    for _, row in df.iterrows():
        if row["type"] == "deposit":
            balance += row["amount"]
        elif row["type"] in ["withdraw", "transfer"]:
            balance -= row["amount"]
        balances.append(balance)

    df["balance"] = balances

    # Plotting
    plt.figure(figsize=(10, 5))
    plt.plot(df["timestamp"], df["balance"], marker='o', linestyle='-')
    plt.title(f" Balance Trend for Account {account_id}")
    plt.xlabel("Date")
    plt.ylabel("Balance ($)")
    plt.grid(True)
    plt.tight_layout()
    plt.show()
