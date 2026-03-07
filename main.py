from dataclasses import dataclass, field 
from enum import Enum
import datetime

# simulate db
InMemoryDB = {'balance': 500, "transactions": []}

class TransactionType(Enum):
    WITHDRAW =  "withdraw"
    DEPOSIT = "deposit"


# Persistance Layer / Gateway / Repository
class AccountRepository:
    def __init__(self, db):
        self.db = db

    def get_account(self):
        balance = self.db.get('balance')
        return Account(balance)
    
    def update_balance(self, account):
        self.db['balance'] = account.balance


class TransactionRepository:
    def __init__(self, db):
        self.db = db

    def get_all_transactions(self):
        return self.db.get('transactions',  [])
    
    def save_transaction(self, obj):
        self.db['transactions'].append(obj)



# Account Entity/Business Rule
class Account:
    def __init__(self, balance):
        self.balance = balance

    def withdraw(self, amount):
        if amount > self.balance:
            raise ValueError("You dont have that much Balance...")
        elif amount <= 0:
            raise ValueError("Invalid Amount")
        else:
            self.balance -= amount
        
    def deposit(self, amount):
        if amount <= 0:
            raise ValueError("Enter a Valid Value...")
        else:
            self.balance += amount
           

# Transaction Entity
@dataclass         
class Transaction:
    txn_type: TransactionType
    amount: float
    balance: float
    timestamp: datetime.datetime = field(default_factory = datetime.datetime.now)

    

# Application Layer
class ATMService:
    def __init__(self, account_repo, txn_repo):
        self.account_repo = account_repo
        self.txn_repo = txn_repo

    def _process_transaction(self, txn_type, amount):
        account = self.account_repo.get_account()
        if txn_type == TransactionType.WITHDRAW:
            account.withdraw(amount)
        elif txn_type == TransactionType.DEPOSIT:
            account.deposit(amount)
        else:
            raise ValueError("Invalid transaction type")
        self.account_repo.update_balance(account)
        transaction = Transaction(txn_type.value, amount, account.balance)
        self.txn_repo.save_transaction(transaction)
        return account.balance
    
    def withdraw(self, amount):
        return self._process_transaction(TransactionType.WITHDRAW, amount)
       
    def deposit(self, amount):
        return self._process_transaction(TransactionType.DEPOSIT, amount)

    def get_balance(self):
        return self.account_repo.get_account().balance
    
    def get_all_transactions(self):
        return self.txn_repo.get_all_transactions()
    

atm_repo = AccountRepository(InMemoryDB)
txn_repo = TransactionRepository(InMemoryDB)
atm_service = ATMService(atm_repo, txn_repo)

amount_to_withdraw = 100
try:
    remaining_balance = atm_service.withdraw(amount_to_withdraw)
    print(f"Amount Withdrawl: ${amount_to_withdraw}")
    print(f"Remaining Balance: ${remaining_balance}")
except ValueError as e:
    print(e)

amount_to_deposit = 500
try:
    remaining_balance = atm_service.deposit(amount_to_deposit)
    print(f"Amount Deposited: ${amount_to_deposit}")
    print(f"Remaining Balance: ${remaining_balance}")
except ValueError as e:
    print(e)

print(InMemoryDB)