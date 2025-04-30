from datetime import datetime

def generate_balance_report(accounts):
    print("\n Account Balance Report")
    for acc_id, acc_data in accounts.items():
        print(f"ID: {acc_id} | Owner: {acc_data['owner']} | Type: {acc_data['type']} | Balance: ${acc_data['balance']:.2f}")

def sort_transactions(transactions, by="amount"):
    print(f"\n Transactions sorted by {by}")
    if by == "amount":
        sorted_tx = sorted(transactions, key=lambda x: x["amount"], reverse=True)
    elif by == "date":
        sorted_tx = sorted(transactions, key=lambda x: datetime.fromisoformat(x["timestamp"]))
    else:
        print(" Invalid sorting key.")
        return

    for tx in sorted_tx:
        print(f"[{tx['timestamp']}] {tx['type'].capitalize()} | ${tx['amount']:.2f} | {tx['description']}")

def search_transactions(transactions, keyword):
    print(f"\n🔍 Transactions containing '{keyword}' or matching ID")
    matches = [
        tx for tx in transactions
        if keyword.lower() in tx.get("description", "").lower()
        or keyword.lower() in tx.get("id", "").lower()
    ]

    if not matches:
        print("No matching transactions found.")
        return

    for tx in matches:
        print(f"[{tx['timestamp']}] {tx['type'].capitalize()} | ${tx['amount']:.2f} | {tx['description']}")
