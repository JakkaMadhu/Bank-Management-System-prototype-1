import mysql.connector

conn = mysql.connector.connect(
    host= "localhost",
    user = "root",
    password = "123456",
    database = "bank_info"
)

curser = conn.cursor()

def txt_record(transaction_type, amount, account_number):
    curser.execute("SELECT IFNULL(MAX(transaction_no),0)+1 FROM transaction_details")
    txt_no = curser.fetchall()[0][0]
    curser.execute("INSERT INTO transaction_details(transaction_no,account_number,transaction_type,amount) VALUES (%s,%s,%s,%s)",(txt_no,account_number,transaction_type,amount))
    conn.commit()

def create_account():
    name = input("Enter Name: ")
    account_number = int(input("Enter account number: "))
    account_type = input("Enter account type (savings/current): ")
    initial_deposit = int(input("Enter Initial deposit: "))
    account_pin = int(input("Set 4-digit PIN: "))
    curser.execute("INSERT INTO user_bank_info(name, account_number,account_type,account_balance,account_pin) VALUES (%s,%s,%s,%s,%s)",(name,account_number,account_type,initial_deposit,account_pin))
    conn.commit()
    print("\n\nAccount Created Successfull....!\n")

def user_login():
    account_number = int(input("Enter Account Number: "))
    account_pin = int(input("Enter 4-digit PIN: "))
    curser.execute("SELECT Name FROM user_bank_info WHERE account_number = %s and account_pin = %s",(account_number, account_pin))
    result = curser.fetchall()
    if result:
        for row in result:
            print(f"\nWelcome, {row[0]}\n")
            user_menu(account_number)
    else:
        print("\nInvalid account number or PIN.\n")

def user_menu(account_number):
    while True:
        option = int(input("1. View Balance\n2. Deposit\n3. Withdraw\n4. View Transactions\n5. Logout\nEnter choice:"))

        if option == 1:
            curser.execute("SELECT account_balance from user_bank_info where account_number = %s",(account_number,))
            result = curser.fetchall()
            print(f"\nCurrent Balance: {result[0][0]}\n")

        elif option == 2:
            deposit_amount = int(input("Enter amount to deposit: "))
            curser.execute("UPDATE user_bank_info SET account_balance = account_balance + %s WHERE account_number = %s",(deposit_amount,account_number))
            conn.commit()
            txt_record("deposit",deposit_amount,account_number)
            print(f"\n{deposit_amount} deposited Successfully!\n")

        elif option == 3:
            withdraw_amount = int(input("Enter amount to withdraw: "))
            curser.execute("SELECT account_balance FROM user_bank_info WHERE account_number = %s",(account_number,))
            current_balance = curser.fetchall()[0][0]
            if current_balance < withdraw_amount:
                print("\nInsufficient Balance.\n")
            else:   
                curser.execute("UPDATE user_bank_info SET account_balance = account_balance - %s WHERE account_number = %s",(withdraw_amount,account_number))
                conn.commit()
                txt_record("withdraw",withdraw_amount,account_number)
                print("\nWithdraw Successfull...!\n")
            
        elif option == 4:
            curser.execute("SELECT transaction_no,transaction_type,amount,date_of_transaction FROM transaction_details WHERE account_number = %s",(account_number,))
            results = curser.fetchall()
            print()
            if results:
                for items in results:
                    print(f"{items[0]} || {items[1]} : {items[2]} || {items[3]}")
            else:
                print("\nNo Transactions Found.\n")
            conn.commit()
            print()
        elif option == 5:
            break
def admin_page():

    admin_name = input("Enter Admin Name: ")
    admin_password = int(input("Enter Admin Password: "))

    curser.execute("SELECT * FROM admin_info")
    rows = curser.fetchall()
    for row in rows:
        if row[0] == admin_name and row[1] == admin_password:
            print("\nAdmin Login Successful!\n")
            print("------>All Customers:\n")  
            curser.execute("SELECT Name,account_number,account_type,account_balance,account_pin,date_of_create FROM user_bank_info")
            details = curser.fetchall()
            for fields in details:
                print(f"Name: {fields[0]} | Account Number: {fields[1]} | Type: {fields[2]} | Balance: {fields[3]} | Created Date: {fields[5]}")
        else:
            print("Invalid Admin Name or Password.\n")
    print("\n\n")
def main():
    while True:
        print("------>Bank Management System<------\n")
        option = int(input("1.Create Account\n2.User Login\n3.Admin Login\n4.Exit\nEnter your Choice: "))
        if option == 1:
            create_account()
        elif option == 2:
            user_login()
        elif option == 3:
            admin_page()
        elif option == 4:
            print("\nExitting.... Thank You\n")
            break
    
if __name__  == "__main__":
    main()
