import tkinter as tk
from tkinter import messagebox, simpledialog
from auth import login, register
from storage import load_data, save_data
from accounts import SavingsAccount, CheckingAccount
from transactions import create_transaction
from reports import generate_balance_report, sort_transactions, search_transactions
from plotting import plot_balance_trend
from utils import generate_account_id
import datetime

# Load data
users, accounts, transactions = load_data()

# Login/Register functions
def handle_login():
    username = username_entry.get()
    password = password_entry.get()
    user = login(users, username, password)
    if user:
        messagebox.showinfo("Login Success", f"Welcome, {username}!")
        root.destroy()
        open_dashboard(user)
    else:
        messagebox.showerror("Login Failed", "Invalid username or password.")

def handle_register():
    username = username_entry.get()
    password = password_entry.get()
    if username in users:
        messagebox.showwarning("Already Exists", "Username already exists.")
        return
    user = register(users, username, password)
    save_data(users, accounts, transactions)
    messagebox.showinfo("Registration Successful", "You can now log in.")

# Dashboard after login
def open_dashboard(user):
    dash = tk.Tk()
    dash.title("\U0001F3E6 Banking Dashboard")

    def create_account():
        acc_type = simpledialog.askstring("Account Type", "Enter account type (savings/checking):")
        if not acc_type or acc_type.lower() not in ["savings", "checking"]:
            messagebox.showerror("Invalid Type", "Must be 'savings' or 'checking'.")
            return
        acc_id = generate_account_id()
        acc = SavingsAccount(acc_id, user["username"]) if acc_type.lower() == "savings" else CheckingAccount(acc_id, user["username"])
        accounts[acc_id] = acc.to_dict()
        user["accounts"].append(acc_id)
        messagebox.showinfo("Account Created", f"New {acc_type} account: {acc_id}")

    def deposit():
        acc_id = simpledialog.askstring("Deposit", "Enter account ID:")
        if acc_id not in user["accounts"]:
            messagebox.showerror("Not Found", "You don't own this account.")
            return
        amount = float(simpledialog.askstring("Amount", "Enter deposit amount:"))
        accounts[acc_id]["balance"] += amount
        transactions.append(create_transaction(acc_id, "deposit", amount, "Deposit"))
        messagebox.showinfo("Success", f"${amount} deposited.")

    def withdraw():
        acc_id = simpledialog.askstring("Withdraw", "Enter account ID:")
        if acc_id not in user["accounts"]:
            messagebox.showerror("Not Found", "You don't own this account.")
            return
        amount = float(simpledialog.askstring("Amount", "Enter withdrawal amount:"))
        if amount > accounts[acc_id]["balance"]:
            messagebox.showerror("Insufficient Funds", "Not enough balance.")
            return
        accounts[acc_id]["balance"] -= amount
        transactions.append(create_transaction(acc_id, "withdraw", amount, "Withdraw"))
        messagebox.showinfo("Success", f"${amount} withdrawn.")

    def transfer():
        from_id = simpledialog.askstring("From", "Enter your account ID:")
        to_id = simpledialog.askstring("To", "Enter recipient account ID:")
        amount = float(simpledialog.askstring("Amount", "Enter amount to transfer:"))
        if from_id not in user["accounts"] or to_id not in accounts:
            messagebox.showerror("Error", "Account not found.")
            return
        if amount > accounts[from_id]["balance"]:
            messagebox.showerror("Insufficient", "Insufficient balance.")
            return
        accounts[from_id]["balance"] -= amount
        accounts[to_id]["balance"] += amount
        transactions.append(create_transaction(from_id, "transfer", amount, f"To {to_id}"))
        transactions.append(create_transaction(to_id, "deposit", amount, f"From {from_id}"))
        messagebox.showinfo("Transferred", f"${amount} sent from {from_id} to {to_id}")

    def view_accounts():
        details = ""
        for acc_id in user["accounts"]:
            acc = accounts[acc_id]
            details += f"{acc_id} - {acc['type']} - Balance: ${acc['balance']:.2f}\n"
        messagebox.showinfo("My Accounts", details or "No accounts.")

    def view_transactions():
        acc_id = simpledialog.askstring("Account ID", "View transactions for account ID:")
        txs = [t for t in transactions if t["account_id"] == acc_id]
        if not txs:
            messagebox.showinfo("None", "No transactions found.")
            return
        output = "\n".join([f"{t['timestamp']} | {t['type']} | ${t['amount']} | {t['description']}" for t in txs])
        messagebox.showinfo("Transactions", output)

    def search_transactions_gui():
        keyword = simpledialog.askstring("Search", "Enter keyword or transaction ID:")
        if not keyword:
            return
        results = [t for t in transactions if keyword.lower() in t["description"].lower() or keyword.lower() in t.get("transaction_id", "").lower()]
        if not results:
            messagebox.showinfo("Search Results", "No transactions found.")
            return
        output = "\n".join([f"{t['timestamp']} | {t['type']} | ${t['amount']} | {t['description']}" for t in results])
        messagebox.showinfo("Search Results", output)

    def sort_transactions_gui():
        key = simpledialog.askstring("Sort", "Sort by (amount/date):")
        if key not in ["amount", "date"]:
            messagebox.showerror("Invalid", "Choose 'amount' or 'date'")
            return
        sorted_txs = sorted(transactions, key=lambda t: t["amount"] if key == "amount" else datetime.datetime.fromisoformat(t["timestamp"]))
        output = "\n".join([f"{t['timestamp']} | {t['type']} | ${t['amount']} | {t['description']}" for t in sorted_txs])
        messagebox.showinfo("Sorted Transactions", output)

    def plot_chart():
        acc_id = simpledialog.askstring("Account ID", "Plot balance trend for account:")
        plot_balance_trend(transactions, acc_id)

    def save_and_exit():
        save_data(users, accounts, transactions)
        messagebox.showinfo("Saved", "Data saved. Exiting.")
        dash.destroy()

    # GUI Buttons
    tk.Label(dash, text=f"Welcome, {user['username']}!", font=("Arial", 14)).pack(pady=10)

    buttons = [
        ("View Accounts", view_accounts),
        ("Create Account", create_account),
        ("Deposit", deposit),
        ("Withdraw", withdraw),
        ("Transfer", transfer),
        ("View Transactions", view_transactions),
        ("Search Transactions", search_transactions_gui),
        ("Sort Transactions", sort_transactions_gui),
        ("Plot Balance Chart", plot_chart),
        ("Save and Exit", save_and_exit),
    ]

    for label, action in buttons:
        tk.Button(dash, text=label, command=action, width=30, pady=5).pack(pady=2)

    dash.mainloop()

# Main login window
root = tk.Tk()
root.title("Banking App - Login/Register")

tk.Label(root, text="Username").grid(row=0, column=0)
tk.Label(root, text="Password").grid(row=1, column=0)

username_entry = tk.Entry(root)
password_entry = tk.Entry(root, show="*")

username_entry.grid(row=0, column=1)
password_entry.grid(row=1, column=1)

tk.Button(root, text="Login", command=handle_login).grid(row=2, column=0)
tk.Button(root, text="Register", command=handle_register).grid(row=2, column=1)

root.mainloop()