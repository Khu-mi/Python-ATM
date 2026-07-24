print("Welcome to ABC BANK")

password=1234
balance=10000
choice=0
pin=int(input("Enter your 4 digit pin: "))

if pin==password:
    while choice !=4:
        print("Menu")
        print("1 == Balance")
        print("2 == deposit")
        print("3 == withdraw")
        print("4 == canceel")

        choice=int(input("Enter your option: "))

        if choice==1:
         print("balance = R", balance)
    #print("Pin correct ")
        elif choice==2:
           dep=int(input("Enter your deposit: R"))
           balance += dep
           print("deposited amount: R" ,dep)
           print("balance = R", balance)

        elif choice==3:
           wit=int(input("Enter your deposit: R"))
           balance -= wit
           print("deposited amount: R" ,wit)
           print("balance = R", balance)

        elif choice==4:
          print("Session ")

    else:
        print("Pin incorrect! Try again")



        #DEF SHOW_BALANCE():
        #PRINT(F"Your balance is R{balance:.2f}")

        def deposit():
           amount = float(input("Enter an amount to be dep"))

           if amount < 0:
              print("That is not a valid amount")
              return 0
           
           else:
              return amount