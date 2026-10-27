"""Entry point for the PyBank ATM program."""

import getpass  # Hides the PIN while it is typed

from account import AccountManager, Authenticator  # Account classes
from logger import ActivityLogger  # Log writer
from transaction import TransactionManager  # Transaction class


def show_start_menu():
    """Print the starting menu."""
    print("\n============================")
    print(" Welcome to PyBank ATM")
    print("============================")
    print("1. Register")
    print("2. Login")
    print("3. Exit")


def show_main_menu():
    """Print the transaction menu."""
    print("\n--- Main Menu ---")
    print("1. Withdraw")
    print("2. Deposit")
    print("3. Transfer (EFT)")
    print("4. View Statement")
    print("5. Logout")


def register_user(accounts):
    """Ask for registration details and create the account."""
    print("\n--- Account Registration ---")
    phone = input("Enter your phone number (10 digits): ").strip()
    pin = getpass.getpass("Create a PIN (4-5 digits): ")  # Hidden
    confirm = getpass.getpass("Confirm PIN: ")  # Hidden
    try:
        number = accounts.register(phone, pin, confirm)  # Do the work
    except ValueError as error:  # Any validation failure
        print("Error:", error)
        return  # Back to the start menu
    print("Registration successful.")
    print(f"Your account number is: {number}")
    print("Please save this number.")
    print("You will need it to receive transfers.")


def login_user(auth):
    """Ask for credentials until login succeeds or the session locks."""
    print("\n--- Login ---")
    while True:  # Keep asking until success or lockout
        phone = input("Phone number: ").strip()
        pin = getpass.getpass("PIN: ")  # Hidden
        try:
            account = auth.login(phone, pin)  # Check the credentials
        except ValueError as error:  # Wrong details, may retry
            print("Error:", error)
            continue
        except PermissionError as error:  # Locked out
            print("Error:", error)
            return None  # Tells main() the session is over
        print("Login successful. Welcome back.")
        return account


def transaction_menu(txn, account):
    """Run the transaction menu until the user logs out."""
    phone = account.phone_number  # Transactions are keyed by phone
    while True:
        show_main_menu()
        choice = input("Select an option: ").strip()
        try:
            if choice == "1":
                text = input("Amount to withdraw: R ")
                balance = txn.withdraw(phone, text)
                print("Withdrawal successful.")
                print(f"New balance: R{balance:.2f}")
            elif choice == "2":
                text = input("Amount to deposit: R ")
                balance = txn.deposit(phone, text)
                print("Deposit successful.")
                print(f"New balance: R{balance:.2f}")
            elif choice == "3":
                print("\n--- EFT Transfer ---")
                dest = input("Recipient account number (8 digits): ")
                text = input("Amount to transfer: R ")
                balance = txn.transfer(phone, dest.strip(), text)
                print("Transfer successful.")
                print(f"Your new balance: R{balance:.2f}")
            elif choice == "4":
                print("\n--- Statement ---")
                lines = txn.get_statement(phone)  # Only my rows
                if not lines:
                    print("No transactions yet.")
                for line in lines:
                    print(line)
            elif choice == "5":
                print("Logged out. Stay safe.")
                return  # Back to the start menu
            else:
                print("Invalid option. Please choose 1 to 5.")
        except ValueError as error:  # Bad amount, no funds, etc.
            print("Error:", error)


def main():
    """Create the objects and run the start menu."""
    logger = ActivityLogger()  # Creates log.txt if missing
    accounts = AccountManager(logger=logger)  # Creates accounts file
    txn = TransactionManager(accounts)  # Creates transactions file
    auth = Authenticator(accounts)  # One login session for the run

    while True:
        show_start_menu()
        choice = input("Select an option: ").strip()
        if choice == "1":
            register_user(accounts)
        elif choice == "2":
            account = login_user(auth)
            if account is None:  # Locked out
                print("Session terminated. Goodbye.")
                break  # Ends the program
            transaction_menu(txn, account)
        elif choice == "3":
            print("Goodbye.")
            break
        else:
            print("Invalid option. Please choose 1 to 3.")


if __name__ == "__main__":
    main()