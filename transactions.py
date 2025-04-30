from datetime import datetime

def create_transaction(account_id, transaction_type, amount, description=""):
    return {
        "account_id": account_id,
        "type": transaction_type,
        "amount": amount,
        "description": description,
        "timestamp": datetime.now().isoformat()
    }

def show_transactions(transactions, account_id=None):
    print("\n Transaction History")
    filtered = [tx for tx in transactions if (account_id is None or tx["account_id"] == account_id)]
    
    if not filtered:
        print("No transactions found.")
        return

    for tx in filtered:
        print(f"[{tx['timestamp']}] {tx['type'].capitalize()} | ${tx['amount']:.2f} | {tx['description']}")
