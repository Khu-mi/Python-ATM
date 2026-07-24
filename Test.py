import account
import random
import hashlib
import csv
import os


class Registration:
    def __init__(self, account):

        self.account = account
     
        # Generate account
    def generate_account_number(self):
        while True:
            account_number = str(random.randint(10000000, 99999999))

            exists = any(
                acc["account_number"] == account_number
                for acc in self.account
            )

            if not exists:
                return account_number
            
# Create account number
registration = Registration("")
account_number = registration.generate_account_number()
print(account_number)




with open("accounts.csv", "r") as file:
    reader = csv.DictReader(file)
    for row in reader:
        if row["account_number"] == account_number:
            found = True
            print("Acount already exists, please enter new account num")
