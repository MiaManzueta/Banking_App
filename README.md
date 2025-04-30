#  Console & GUI Banking App

A simple yet functional Python banking application that allows users to manage savings and checking accounts, perform transactions, generate reports, and visualize data. It supports both **console** and **Tkinter GUI** interfaces.

---

##  How to Run the Application

### Console Version
1. Ensure you have **Python 3.10+** installed.
2. Run the main application:
   ```bash
   python main.py
   ```

### GUI Version (Tkinter)
1. Ensure you have **Tkinter** (usually comes with Python).
2. Run the GUI interface:
   ```bash
   python gui.py
   ```

---

##  Features

###  Authentication
- User registration and secure login with password masking.

###  Account Management
- Create **Savings** or **Checking** accounts.
- View all personal account details.

###  Transactions
- **Deposit**, **Withdraw**, and **Transfer** between accounts.
- All transactions are timestamped and logged.

###  Reporting & Analysis
- Generate a **balance report** for all accounts.
- **Sort transactions** by amount or date.
- **Search** transactions by keyword or ID.
- **Plot balance trends** using matplotlib.

###  Data Persistence
- All user, account, and transaction data is saved locally in JSON format.

---

##  Challenges & Reflections

- **Data structure design** was crucial for supporting both the console and GUI interfaces.
- Managing consistent updates to the shared state (`users`, `accounts`, `transactions`) across both interfaces required careful handling.
- Integrating **Tkinter** for GUI presented layout and usability challenges, but provided a more intuitive experience.
- Ensuring **input validation** and **error handling** improved the application's robustness.

This project was a great learning experience in combining **OOP**, **file I/O**, **GUI development**, and **data visualization** in Python.

---

##  File Structure

```
.
├── main.py           # Console interface
├── gui.py            # GUI interface (Tkinter)
├── auth.py           # Login and registration logic
├── accounts.py       # Account classes
├── transactions.py   # Transaction handling
├── storage.py        # Data loading/saving
├── reports.py        # Reporting and analysis
├── plotting.py       # Chart plotting with matplotlib
├── utils.py          # Helpers (e.g., ID generation)
├── data.json         # Saved app data
└── README.md         # This file
```

---

##  Requirements

- Python 3.10+
- `matplotlib` (for chart plotting)
```bash
pip install matplotlib
```

---

##  Feedback

Feel free to contribute or suggest improvements. Happy banking! 
