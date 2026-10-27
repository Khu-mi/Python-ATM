"""Scratch file for testing the ATM classes. Not part of the project."""

from account import AccountManager  # Account class
from transaction import TransactionManager # Transaction class

accounts = AccountManager()  # Creates account_balances.txt, log.txt
txn = TransactionManager(accounts)  # Creates transactions.txt

# Register two users (ignore errors if they already exist)
for phone in ("0821234567", "0829999999"):
    try:
        accounts.register(phone, "1234", "1234")
    except ValueError as error:
        print("Register:", error)

me = "0821234567"  # Sender
other = accounts.find_by_phone("0829999999").account_number  # Recipient


def attempt(label, action):
    """Run one test action and print the result or the error."""
    try:
        print(label, "->", action())
    except ValueError as error:
        print(label, "-> Error:", error)


attempt("Deposit 500", lambda: txn.deposit(me, "500"))
attempt("Withdraw 100", lambda: txn.withdraw(me, "100"))
attempt("Withdraw 1000", lambda: txn.withdraw(me, "1000"))
attempt("Deposit abc", lambda: txn.deposit(me, "abc"))
attempt("EFT bad format", lambda: txn.transfer(me, "1234", "50"))
attempt("EFT unknown", lambda: txn.transfer(me, "99999999", "50"))
own = accounts.find_by_phone(me).account_number
attempt("EFT to self", lambda: txn.transfer(me, own, "50"))
attempt("EFT 150", lambda: txn.transfer(me, other, "150"))

print("--- My statement ---")
for line in txn.get_statement(me):
    print(line)
print("--- Their statement ---")
for line in txn.get_statement("0829999999"):
    print(line)