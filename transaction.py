"""Transaction handling for the ATM system."""

import csv  # Reads and writes CSV files safely
import math  # Lets us reject nan and infinity amounts
import os  # Lets us check if a file exists
from datetime import datetime  # Gives us timestamps


class TransactionManager:
    """Performs transactions and records them in a CSV file."""

    HEADERS = ["timestamp", "phone_number", "transaction_type",
               "amount", "balance_after"]  # Columns in the file
    CREDITS = ("DEPOSIT", "EFT IN")  # Types that add money

    def __init__(self, account_manager, filename="transactions.txt"):
        """Store the account manager and create the file if missing."""
        self.account_manager = account_manager  # Gives file access
        self.filename = filename  # File that stores transactions
        self._create_file_if_missing()  # Make sure the file exists

    def _create_file_if_missing(self):
        """Create the transactions file with a header row if missing."""
        if not os.path.exists(self.filename):  # Not there yet?
            with open(self.filename, "w", newline="") as file:
                writer = csv.writer(file)  # Tool that writes CSV rows
                writer.writerow(self.HEADERS)  # Write the column names

    def _record(self, phone_number, transaction_type, amount, balance):
        """Append one timestamped transaction row to the file."""
        now = datetime.now()  # Current date and time
        timestamp = now.strftime("%Y-%m-%d %H:%M:%S")  # Format as text
        with open(self.filename, "a", newline="") as file:  # Append
            writer = csv.writer(file)  # Tool that writes CSV rows
            writer.writerow([timestamp, phone_number, transaction_type,
                             f"{amount:.2f}", f"{balance:.2f}"])

    @staticmethod
    def _parse_amount(text):
        """Convert typed text to a valid positive amount."""
        try:
            amount = round(float(text), 2)  # Text to number, 2 decimals
        except ValueError:
            raise ValueError("Amount must be a number.") from None
        if not math.isfinite(amount) or amount <= 0:  # nan, inf, zero
            raise ValueError("Amount must be greater than zero.")
        return amount

    @staticmethod
    def _find(accounts, attribute, value):
        """Return the account whose attribute equals value, or None."""
        for account in accounts:  # Check every account in turn
            if getattr(account, attribute) == value:
                return account  # Found a match
        return None  # No match anywhere

    def deposit(self, phone_number, amount_text):
        """Add money to an account and return the new balance."""
        amount = self._parse_amount(amount_text)  # Validate first
        accounts = self.account_manager.load_accounts()  # Read
        account = self._find(accounts, "phone_number", phone_number)
        account.balance = round(account.balance + amount, 2)  # Modify
        self.account_manager.save_accounts(accounts)  # Write back
        self._record(phone_number, "DEPOSIT", amount, account.balance)
        return account.balance

    def withdraw(self, phone_number, amount_text):
        """Remove money from an account and return the new balance."""
        amount = self._parse_amount(amount_text)  # Validate first
        accounts = self.account_manager.load_accounts()  # Read
        account = self._find(accounts, "phone_number", phone_number)
        if amount > account.balance:  # Not enough money?
            raise ValueError("Insufficient funds.")
        account.balance = round(account.balance - amount, 2)  # Modify
        self.account_manager.save_accounts(accounts)  # Write back
        self._record(phone_number, "WITHDRAWAL", amount, account.balance)
        return account.balance

    def transfer(self, phone_number, destination, amount_text):
        """Send money to another account and return the new balance."""
        # Format check comes BEFORE any lookup, as the brief requires
        if not (destination.isdigit() and len(destination) == 8):
            raise ValueError("Account number must be exactly 8 digits.")
        amount = self._parse_amount(amount_text)  # Validate the amount
        accounts = self.account_manager.load_accounts()  # Read
        sender = self._find(accounts, "phone_number", phone_number)
        if sender.account_number == destination:  # Sending to yourself?
            raise ValueError("You cannot transfer to your own account.")
        recipient = self._find(accounts, "account_number", destination)
        if recipient is None:  # Number not in the file
            raise ValueError("Account not found. Please check the "
                             "account number and try again.")
        if amount > sender.balance:  # Not enough money?
            raise ValueError("Insufficient funds.")
        sender.balance = round(sender.balance - amount, 2)  # Modify both
        recipient.balance = round(recipient.balance + amount, 2)
        self.account_manager.save_accounts(accounts)  # One write, both
        self._record(phone_number, "EFT OUT", amount, sender.balance)
        self._record(recipient.phone_number, "EFT IN", amount,
                     recipient.balance)
        return sender.balance

    def get_statement(self, phone_number):
        """Return this account's transactions as a list of text lines."""
        lines = []  # Will hold one line per transaction
        with open(self.filename, "r", newline="") as file:
            reader = csv.DictReader(file)  # Each row becomes a dict
            for row in reader:  # Go through every transaction
                if row["phone_number"] != phone_number:
                    continue  # Skip other people's rows
                kind = row["transaction_type"]  # Shorter name
                sign = "+" if kind in self.CREDITS else "-"  # + or -
                lines.append(
                    f"{row['timestamp']} | {kind} | "
                    f"{sign}R{row['amount']} | "
                    f"Balance: R{row['balance_after']}")
        return lines