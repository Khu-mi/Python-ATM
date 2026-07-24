#import account
import random
import hashlib
import csv
import os
import datetime
# import account

def generate_account_number():
    while True:
        account_number = str(random.randint(10000000, 99999999))
        return account_number

def register_log_event (phone, event_type):
    datetime_now = datetime.datetime.now()
    with open("logs.csv", "a", newline="") as file:
        writer = csv.writer(file)
        writer.writerow([ 
            datetime_now,
            phone,
            event_type
        ])



#Create Files
acc_column_headers = ["account_number", "phone_number", "hashed_PIN", "balance"]  
log_column_headers = ["datetime", "phone_number", "event_type"]

#Accounts.csv
if not os.path.exists("accounts.csv"):
    with open("accounts.csv", "w", newline="") as file:
        writer = csv.DictWriter(file, fieldnames=acc_column_headers)
        writer.writeheader()

#log.txt
if not os.path.exists("logs.csv"):
    datetime_now = datetime.datetime.now()  
    with open("logs.csv", "w", newline="") as file:
        writer = csv.DictWriter(file, fieldnames=log_column_headers)
        writer.writeheader()
        writer.writerow({
            "datetime": datetime_now,
            "phone_number": "N/A",
            "event_type" : "Log File Created"
        })


def main_menu():
    print("""
        ========================================================================================================
                                                WELCOME TO KBM BANK
                                                    [MAIN MENUE]
        ========================================================================================================
        1.Register
        2.Login
        3.Exit
        """)


    options = [1,2,3]
    choice = int(input("Choose an option: "))
    if choice not in options:
        print("Invalid option")
        
    return choice

choice = main_menu()

pin = ()
if choice == 1:

    # Register Phone Number
    # Keep asking until valid ee number
    while True:
        phone = input("Enter your phone number: ")
        if len(phone) != 10:
            print("Number must be 10 digits, try again")
            continue

        found = False
        with open("accounts.csv", "r") as file:
            reader = csv.DictReader(file)
            for row in reader:
                if row["phone_number"] == phone:
                    found = True
                    print("Acount already exists, please enter new Number")
        if not found:
            break 
    
    #Register PIN
    while True:
        pin = input("Create PIN (4-5 digits): ")
        if not (4 <= len(pin) <= 5):
            print(f"Error: PIN must be 4-5 digits. You entered {len(pin)} digit(s).")
        else:
            break  # valid PIN length, exit loop
    # PIN Confirmation: Keep asking until PIN is confirmed
    while True:
        conpin = input("Confirm PIN: ")
        if conpin != pin:
            print("PIN Invalid, try again")
        else:
            break  # PIN matched, exit loop
    #Hash PIN
    pinhash = hashlib.sha256(pin.encode()).hexdigest()  
    
    # Create account number
    while True:
        # registration = Registration("")
        account_number = generate_account_number()
        #print(account_number) #debug
        found = False

        with open("accounts.csv", "r") as file:
            reader = csv.DictReader(file)
            for row in reader:
                if row["account_number"] == account_number:
                    found = True
                    print("Acount already exists. Generating a new Acc Number")
                    break
        if not found:
            break

    with open("accounts.csv", "a", newline="") as file:
     writer = csv.writer(file)
     writer.writerow([ 
      account_number,
      phone,
      pinhash,
      0
      ]) 

    # print(phone) #debug
    # print(pinhash) #debug
    # print(account_number) #debug
    
    #Log entry
    register_log_event(phone, "Account Registered")

    print("Registration Successful")
    choice = main_menu()
    options = [1,2,3]
    choice = int(input("Choose an option: "))

if choice == 2:
    print("You are about to login")

    # Verifying Login Phone Number
    while True:
        phone = input("Enter your phone number: ")
        if len(phone) != 10:
            print("Number must be 10 digits, try again")
            continue

        found = False
        with open("accounts.csv", "r") as file:
            reader = csv.DictReader(file)
            for row in reader:
                if row["phone_number"] == phone:
                    login_pin = row["hashed_PIN"]
                    found = True
                    break
        if not found:
            print("Acount does not exists, please register or try again")
        else:
            #print(f"Login Successfull. Welcome {phone}" )  #debug
            break
    # Verifying Login Hashed Pin
    attempts = 0
    while attempts < 3 :
        pin = input("Enter Login PIN (4-5 digits): ")
        if not (4 <= len(pin) <= 5):
            attempts += 1
            print(f"Error: PIN must be 4-5 digits. You entered {len(pin)} digit(s). This is attempt number {attempts}.")
            print("Please try again.")
            #Log entry
            register_log_event(phone, f"Incorrect pin length. {len(pin)} digit(s)")
            continue

        # Hasshed PIN Confirmation: Keep asking until PIN is confirmed
        pinhash = hashlib.sha256(pin.encode()).hexdigest()  
        if pinhash == login_pin:
            print("Login successful. Welcome back.")
            #Log entry
            register_log_event(phone, "Login Successful")
            break

        else:
            attempts += 1
            print(f"Incorrect pin. Attempt Number: {attempts}")
            print("Please try again.")
            #Log entry
            register_log_event(phone, f"Login Failed. Incorrect pin. Attempt #{attempts} ")
    if attempts == 3:
        print("Too many failed attempts. Account locked.")
        print("Contact the your nearest branch")
        #Log entry
        register_log_event(phone, f"Login Failed. Exceeded attemtpts.")

    from account import account_menu
    account_menu(phone)

elif choice == 3:
    print("Thank you for using KBM BANK. See you soon.")
    exit()
