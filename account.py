import os
import csv
import hashlib
from datetime import datetime


class Account:
    def __init__(self, phone):
        self.phone = phone
        # self.balance = balance

    def account_number (self):
        with open("accounts.csv", "r") as file:
            reader = csv.DictReader(file)
            for row in reader:
                if row["phone_number"] == self.phone:
                    account_number = row["account_number"]
                    return account_number

    def account_balance (self):
        with open("accounts.csv", "r") as file:
            reader = csv.DictReader(file)
            for row in reader:
                if row["phone_number"] == self.phone:
                    account_balance = row["balance"]
                    return float([account_balance])
                

                
    



class Transaction:
    def __init__(self, account ):
        self.account = account
        self.balance = account.account_balance()

    def deposit(self,amount):
           self.balance += amount
           ##self.account.update_balance(self,balance)


           now = datetime.now()
           print("Deposit Done")
           print("Time:", now)
           print("Deposit Done", self.balance)

          
           log_transaction(self.account.phone, "DEPOSIT", amount, self.balance)


           

    def withdraw(self,amount):
           if amount <= self.balance:
                  self.balance -= amount
                  self.account.update_balance(self.balance)

                  now = datetime.now()
                  print("Withdrwal Done")
                  print("Time:", now)
                  print("Deposit Done", self.balance)
                  print("Withdrawal Done", self.balance)


                

           else:
                  print("NO money")

    def show_balance(self):
        print("Current Balance", self.balance)

def register_log_event (phone, event_type):
    datetime_now = datetime.now()

    with open("logs.csv", "a", newline="") as file:
        writer = csv.writer(file)
        writer.writerow([ 
            datetime_now,
            phone,
            event_type
        ])

def log_transaction(phone, transaction_type, amount, balance):
    timestamp = datetime.now()

    with open("transactions.txt", "a") as file:
        file.write(f"{timestamp} | {phone} | {transaction_type} | {amount} | {balance}\n")
# log_transaction_column_headers = ["Timestamp", "phone_number", "transaction_type", "amount"]  

if not os.path.exists("transactions.txt"):
    with open("transactions.txt", "w") as file:
         file.write("timestamp | phone_number | transaction_type | amount | balance\n")

def view_statement(phone):
    print("\n--- Statement ---")

    with open("transactions.txt", "r") as file:
        for line in file:
            if phone in line:
                print(line.strip())


def account_menu(phone):

    #Define Account Object
    account_number = Account(phone)
    user = account_number.account_number()
    balance = account_number.account_balance()
    print(user)
    print(balance)

    if not os.path.exists("transactions.txt"):
     with open("transactions.txt", "w") as file:
        file.write("timestamp | phone_number | transaction_type | amount | balance\n")

    print("""
        ========================================================================================================
                                                WELCOME TO KBM BANK
                                                 [ACCOUNTS MENUE]
        ========================================================================================================

        1.Deposit
        2.Withdraw  
        3.Transfer (EFT)  
        4.View Statement  
        5.Logout  
        """)

    # options = [0,1,2,3,4,5]    
    # choice = int(input("Choose an option: "))
    # if choice not in options:
    #     print("Invalid option")
    #     return account_menu()
    # return choice

# choice = account_menu()
choice = ()
account =()
phone =() #"0711869917" #debug

#Log entry
#register_log_event(phone, "Account registered")

if choice == 0:
    account_number = Account(phone)
    account_balance = Account(phone)
    user = account_number.account_number()
    balance = account_number.account_balance()
    print(user)
    print(balance)

if choice == 1:
    deposit = float(input("Amount to deposit: R"))
    Transaction.deposit(deposit)
    register_log_event(phone, f"You have deposited{deposit}")

elif choice == 2:
    withdraw = float(input("Amount to withdraw:R "))
    Transaction.withdraw(withdraw)
    register_log_event(phone, f"You have withdrew{account.withdraw}")

elif choice == 3:
    print("---EFT Coming Soon")

elif choice == 4:
    print("Logged out")
    register_log_event(phone, f"You have logged out.")

else:
    print("Invalid option")
    register_log_event(phone, f"Entred invlaid option")





