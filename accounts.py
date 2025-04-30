from datetime import datetime

class Account:
    def __init__(self, account_id, owner, balance=0.0):
        self.account_id = account_id
        self.owner = owner
        self.balance = balance
        self.created_at = datetime.now().isoformat()

    def deposit(self, amount):
        if amount > 0:
            self.balance += amount
            return True
        return False

    def withdraw(self, amount):
        if 0 < amount <= self.balance:
            self.balance -= amount
            return True
        return False

    def to_dict(self):
        return {
            "account_id": self.account_id,
            "owner": self.owner,
            "balance": self.balance,
            "created_at": self.created_at,
            "type": self.__class__.__name__
        }

    def __str__(self):
        return f"{self.__class__.__name__} | ID: {self.account_id} | Owner: {self.owner} | Balance: ${self.balance:.2f}"

class SavingsAccount(Account):
    def __init__(self, account_id, owner, balance=0.0, interest_rate=0.02):
        super().__init__(account_id, owner, balance)
        self.interest_rate = interest_rate

    def apply_interest(self):
        self.balance += self.balance * self.interest_rate

    def to_dict(self):
        data = super().to_dict()
        data["interest_rate"] = self.interest_rate
        return data

class CheckingAccount(Account):
    def __init__(self, account_id, owner, balance=0.0, overdraft_limit=100.0):
        super().__init__(account_id, owner, balance)
        self.overdraft_limit = overdraft_limit

    def withdraw(self, amount):
        if 0 < amount <= self.balance + self.overdraft_limit:
            self.balance -= amount
            return True
        return False

    def to_dict(self):
        data = super().to_dict()
        data["overdraft_limit"] = self.overdraft_limit
        return data
