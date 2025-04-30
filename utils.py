import random
import string

def generate_account_id():
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=8))

def show_main_menu():
    print("\n MAIN MENU")
    print("1. Create New Account")
    print("2. View My Accounts")
    print("3. Deposit Funds")
    print("4. Withdraw Funds")
    print("5. Transfer Funds")
    print("6. View Transaction History")
    print("7. View Balance Report")
    print("8. Plot Balance Trend")
    print("9. Sort Transactions")
    print("10. Search Transactions")
    print("0. Save and Exit")
