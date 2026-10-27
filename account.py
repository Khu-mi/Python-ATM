"""Account data and account file management for the ATM system."""

import csv  # Reads and writes CSV files safely
import os  # Lets us check if a file exists
import random  # Generates the random account numbers

from logger import ActivityLogger  # Our log writer
from security import PinSecurity  # Our PIN hashing


class Account:
    """Represents one bank account."""

    def __init__(self, account_number, phone_number,
                 hashed_pin, balance=0.0):
        """Store the details of one account."""
        self.account_number = account_number  # 8-digit number
        self.phone_number = phone_number  # Login credential
        self.hashed_pin = hashed_pin  # 'salt$hash', never the raw PIN
        self.balance = float(balance)  # CSV gives text, so convert

    def to_row(self):
        """Return this account as a dictionary ready for the CSV."""
        return {
            "account_number": self.account_number,
            "phone_number": self.phone_number,
            "hashed_pin": self.hashed_pin,
            "balance": f"{self.balance:.2f}",  # Always 2 decimals
        }


class AccountManager:
    """Registers accounts and reads and writes the accounts file."""

    HEADERS = ["account_number", "phone_number", "hashed_pin", "balance"]

    def __init__(self, filename="account_balances.txt", logger=None):
        """Set up the file name and logger, then create the file."""
        self.filename = filename  # File that stores the accounts
        self.logger = logger or ActivityLogger()  # Use given or new one
        self._create_file_if_missing()  # Make sure the file exists

    def _create_file_if_missing(self):
        """Create the accounts file with a header row if missing."""
        if not os.path.exists(self.filename):  # Not there yet?
            with open(self.filename, "w", newline="") as file:
                writer = csv.DictWriter(file, fieldnames=self.HEADERS)
                writer.writeheader()  # Write the column names

    def load_accounts(self):
        """Read the file and return a list of Account objects."""
        accounts = []  # Will hold every account found
        with open(self.filename, "r", newline="") as file:
            reader = csv.DictReader(file)  # Each row becomes a dict
            for row in reader:  # Go through every row
                accounts.append(Account(
                    row["account_number"],
                    row["phone_number"],
                    row["hashed_pin"],
                    row["balance"],
                ))
        return accounts

    def save_accounts(self, accounts):
        """Overwrite the file with the given list of accounts."""
        with open(self.filename, "w", newline="") as file:
            writer = csv.DictWriter(file, fieldnames=self.HEADERS)
            writer.writeheader()  # Column names first
            for account in accounts:  # Then one row per account
                writer.writerow(account.to_row())

    def find_by_phone(self, phone_number):
        """Return the Account with this phone number, or None."""
        for account in self.load_accounts():
            if account.phone_number == phone_number:
                return account  # Found a match
        return None  # No match anywhere

    def find_by_account_number(self, account_number):
        """Return the Account with this account number, or None."""
        for account in self.load_accounts():
            if account.account_number == account_number:
                return account  # Found a match
        return None  # No match anywhere

    def _generate_account_number(self):
        """Return a random 8-digit number that is not already used."""
        used = {a.account_number for a in self.load_accounts()}  # A set
        while True:  # Keep trying until we find a free number
            number = str(random.randint(10000000, 99999999))
            if number not in used:  # Not taken by anyone?
                return number  # Safe to use

    def register(self, phone_number, pin, confirm_pin):
        """Validate and create a new account, returning its number.

        Raises ValueError with a clear message if anything is invalid.
        """
        if not (phone_number.isdigit() and len(phone_number) == 10):
            raise ValueError("Phone number must be exactly 10 digits.")
        if not (pin.isdigit() and len(pin) in (4, 5)):
            raise ValueError("PIN must be 4 or 5 digits.")
        if pin != confirm_pin:
            raise ValueError("PINs do not match.")
        if self.find_by_phone(phone_number) is not None:
            raise ValueError("An account with this phone number exists.")

        account = Account(
            self._generate_account_number(),  # Unique 8-digit number
            phone_number,
            PinSecurity.hash_pin(pin),  # Only the hash is kept
        )
        with open(self.filename, "a", newline="") as file:  # Append
            writer = csv.DictWriter(file, fieldnames=self.HEADERS)
            writer.writerow(account.to_row())  # Add the new account
        self.logger.log_event(phone_number, "REGISTERED")  # Log it
        return account.account_number  # Shown to the user once


class Authenticator:
    """Handles login for one session and enforces the lockout."""

    MAX_ATTEMPTS = 3  # Consecutive failures allowed

    def __init__(self, account_manager):
        """Store the manager and start with zero failed attempts."""
        self.account_manager = account_manager  # Used to find accounts
        self.logger = account_manager.logger  # Reuse the same logger
        self.failed_attempts = 0  # Consecutive failures so far

    def is_locked(self):
        """Return True once the maximum failures is reached."""
        return self.failed_attempts >= self.MAX_ATTEMPTS

    def login(self, phone_number, pin):
        """Return the Account if the credentials are correct.

        Raises ValueError for a failed attempt and PermissionError
        once the session is locked.
        """
        if self.is_locked():  # Block further attempts
            raise PermissionError("Too many failed attempts.")

        account = self.account_manager.find_by_phone(phone_number)
        if account is not None and PinSecurity.verify_pin(
                pin, account.hashed_pin):  # Phone found AND PIN matches
            self.failed_attempts = 0  # Success resets the counter
            self.logger.log_event(phone_number, "LOGIN_SUCCESS")
            return account

        self.failed_attempts += 1  # Count this failure
        self.logger.log_event(phone_number, "LOGIN_FAILED")
        if self.is_locked():  # Was that the third strike?
            raise PermissionError("Too many failed attempts.")
        left = self.MAX_ATTEMPTS - self.failed_attempts  # Tries remaining
        raise ValueError(
            f"Invalid phone number or PIN. {left} attempt(s) left.")

    