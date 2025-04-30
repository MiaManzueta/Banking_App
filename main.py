from auth import login, register
from accounts import SavingsAccount, CheckingAccount
from transactions import create_transaction, show_transactions
from storage import load_data, save_data
from reports import generate_balance_report, sort_transactions, search_transactions
from plotting import plot_balance_trend
from utils import generate_account_id, show_main_menu
import getpass

def main():
    users, accounts, transactions = load_data()

    print(" Welcome to Console Banking App")
    while True:
        print("\n1. Login\n2. Register\n0. Exit")
        choice = input("Choose an option: ")
        if choice == "1":
            username = input("Enter username: ")
            password = getpass.getpass("Enter password: ")
            current_user = login(users, username, password)
            if current_user:
                print(" Login successful.")
            else:
                print(" Invalid credentials.")
        elif choice == "2":
            username = input("Choose username: ")
            if username in users:
                print(" Username already exists.")
                continue
            password = getpass.getpass("Choose password: ")
            confirm = getpass.getpass("Confirm password: ")
            if password != confirm:
                print(" Passwords do not match.")
                continue
            current_user = register(users, username, password)
            print(" Registration successful.")
        elif choice == "0":
            print(" Goodbye!")
            return
        else:
            print(" Invalid choice.")
            continue

        if current_user:
            break

    while True:
        show_main_menu()
        option = input("Select an option: ")

        if option == "1":  # Create New Account
            acc_type = input("Account Type (savings/checking): ").lower()
            acc_id = generate_account_id()
            if acc_type == "savings":
                account = SavingsAccount(acc_id, current_user["username"])
            elif acc_type == "checking":
                account = CheckingAccount(acc_id, current_user["username"])
            else:
                print(" Invalid account type.")
                continue
            accounts[acc_id] = account.to_dict()
            current_user["accounts"].append(acc_id)
            print(f" Account created with ID: {acc_id}")

        elif option == "2":  # View Accounts
            for acc_id in current_user["accounts"]:
                print(accounts[acc_id])

        elif option == "3":  # Deposit
            acc_id = input("Enter account ID: ")
            if acc_id not in current_user["accounts"]:
                print(" Account not found.")
                continue
            amount = float(input("Enter deposit amount: "))
            accounts[acc_id]["balance"] += amount
            transactions.append(create_transaction(acc_id, "deposit", amount, "Deposit"))
            print(" Deposit successful.")

        elif option == "4":  # Withdraw
            acc_id = input("Enter account ID: ")
            if acc_id not in current_user["accounts"]:
                print(" Account not found.")
                continue
            amount = float(input("Enter withdrawal amount: "))
            if amount > accounts[acc_id]["balance"]:
                print(" Insufficient funds.")
                continue
            accounts[acc_id]["balance"] -= amount
            transactions.append(create_transaction(acc_id, "withdraw", amount, "Withdrawal"))
            print(" Withdrawal successful.")

        elif option == "5":  # Transfer
            from_id = input("From account ID: ")
            to_id = input("To account ID: ")
            if from_id not in current_user["accounts"] or to_id not in accounts:
                print(" Invalid accounts.")
                continue
            amount = float(input("Enter transfer amount: "))
            if amount > accounts[from_id]["balance"]:
                print(" Insufficient funds.")
                continue
            accounts[from_id]["balance"] -= amount
            accounts[to_id]["balance"] += amount
            transactions.append(create_transaction(from_id, "transfer", amount, f"Transfer to {to_id}"))
            transactions.append(create_transaction(to_id, "deposit", amount, f"Transfer from {from_id}"))
            print(" Transfer complete.")

        elif option == "6":  # View Transactions
            show_transactions(transactions)

        elif option == "7":  # Balance Report
            generate_balance_report(accounts)

        elif option == "8":  # Plot Trend
            acc_id = input("Account ID to plot: ")
            if acc_id not in accounts:
                print(" Account not found.")
                continue
            plot_balance_trend(transactions, acc_id)

        elif option == "9":  # Sort Transactions
            key = input("Sort by (amount/date): ").lower()
            sort_transactions(transactions, key)

        elif option == "10":  # Search Transactions
            keyword = input("Enter keyword or transaction ID to search: ")
            search_transactions(transactions, keyword)

        elif option == "0":  # Exit and Save
            save_data(users, accounts, transactions)
            print(" Data saved. Goodbye!")
            break

        else:
            print(" Invalid option.")

if __name__ == "__main__":
    main()
