from sqlite3 import *
import string
import hashlib

# Global variable to track the user login status
login_status = False
current_user = None

def hash_password(password: str) -> str:
    """Hash the password using SHA256."""
    return hashlib.sha256(password.encode()).hexdigest()

def checkName(name: str):
    """Check if the name contains only alphabets and spaces."""
    alphabet = string.ascii_letters  # Set of valid characters for names (letters and spaces)
    for i in name:
        if i not in alphabet and i != " ":  # Check if each character is valid
            print("Name must be alphabetic")
            return False  # Return False if any invalid character is found
    return True  # Return True if all characters are valid

def checkCardID(card_id: str):
    """Check if the card_id is valid (must be 8 digits)."""
    if not card_id.isdigit():  # Ensure the card_id consists only of digits
        print("Invalid card id input")
        return False
    
    if len(card_id) != 8:  # Ensure the card_id has exactly 8 digits
        print("Invalid card id input")
        return False
    
    return True  # Return True if the card_id is valid

def checkPassword(password: str, confirmPassword: str):
    """Check if the password meets the requirements (min length and matching passwords)."""
    if len(password) < 6:  # Password should be at least 6 characters long
        print("Password too short!")
        return False
    
    if password != confirmPassword:  # Ensure both passwords match
        print("Passwords do not match!")
        return False
    
    return True  # Return True if the password is valid

def register():
    """Handle user registration including name, card_id, and password validation."""
    global login_status  # To track the login status after registration
    try:
        print("\nRegister: ")
        name = input("Enter your name: ")
        card_id = input("Enter your card id: ")
        password = input("Password: ")
        confirmPassword = input("Confirm password: ")
        print("\n")
    except ValueError:
        print("Invalid input!")
        return
    
    # Validate name, card_id, and password
    checkedName = checkName(name)
    checkedCardID = checkCardID(card_id)
    checkedPassword = checkPassword(password, confirmPassword)
    
    # Proceed with registration if all checks pass
    if checkedName and checkedCardID and checkedPassword:
        try:
            db = connect("ATMdatabase.db")
            cursor = db.cursor()

            # Check if user or card_id already exists
            cursor.execute("SELECT name FROM users WHERE name = ?", (name,))
            checkExistUser = cursor.fetchone()
            
            cursor.execute("SELECT card_id FROM users WHERE card_id = ?", (card_id,))
            checkExistCardID = cursor.fetchone()

            if checkExistUser or checkExistCardID:  # If user or card_id already exists, show an error
                print("Username or card id already exists!")
            else:
                hashed_password = hash_password(password)  # Store hashed password in database
                cursor.execute("INSERT INTO users (name, card_id, password) VALUES(?, ?, ?)", 
                               (name, card_id, hashed_password))
                db.commit()
                print("Registration successful!")
        except Error as e:
            print(f"Database error: {e}")
        finally:
            db.close()
        login()  # Call login after successful registration
    else:
        print("Invalid input or password mismatch!")

def login():
    """Handle user login and check credentials."""
    global login_status, current_user  # To manage login status and store card_id
    try:
        print("\nLogin: ")
        card_id = input("Enter your card id: ")
        password = input("Password: ")
        print("\n")
    except ValueError:
        print("Invalid input!")
        return
    
    try:
        db = connect("ATMdatabase.db")
        cursor = db.cursor()
        
        # Check if the card_id exists in the database
        cursor.execute("SELECT name, password FROM users WHERE card_id = ?", (card_id,))
        user = cursor.fetchone()

        if user:
            # Compare password (hashed) with the stored one
            stored_name, stored_hashed_password = user
            hashed_input_password = hash_password(password)
            
            if stored_hashed_password == hashed_input_password:  # If password matches
                login_status = True
                current_user = card_id  # Store card_id of logged in user
                print(f"Welcome, {stored_name}!")
            else:
                print("Incorrect password!")  # Password mismatch
        else:
            print("Card ID not found!")  # If card_id is not found in the database
        
    except Error as e:
        print(f"Database error: {e}")
    finally:
        db.close()

def checkBalance(card_id: str):
    """Check the current balance of the given card_id."""
    try:
        db = connect("ATMdatabase.db")
        cursor = db.cursor()
        cursor.execute("SELECT balance FROM users WHERE card_id = ?", (card_id,))
        balance = cursor.fetchone()
        
        if balance is None:  # If card_id is not found, return None
            print("Card ID not found.")
            return None
        
        return balance[0]  # Return just the balance value, not the entire tuple
    except Error as e:
        print(f"Database error: {e}")
    finally:
        db.close()

def withdraw(card_id: str):
    """Handle withdrawal for the logged-in user."""
    currentBalance = checkBalance(current_user)  # Get the current balance of the user
    print(f"\nBalance: {currentBalance}")
    withdrawAmount = int(input("Enter amount to withdraw: "))
    
    if withdrawAmount > currentBalance:  # Check if the user has sufficient funds
        print("Insufficient funds.")
    else:
        currentBalance -= withdrawAmount  # Deduct the withdrawal amount
        
        try:
            db = connect("ATMdatabase.db")
            cursor = db.cursor()
            cursor.execute("UPDATE users SET balance = ? WHERE card_id = ?", (currentBalance, card_id,))
            db.commit()  # Commit the changes to the database
            print(f"Withdrawal successful. New balance: {currentBalance}")
        except Error as e:
            print(f"Database error: {e}")
        finally:
            db.close()

def deposit(card_id: str):
    """Handle deposit for the logged-in user."""
    currentBalance = checkBalance(current_user)  # Get the current balance of the user
    print(f"\nBalance: {currentBalance}")
    
    depositAmount = int(input("Enter amount to deposit: "))
    currentBalance += depositAmount  # Add the deposit amount to the current balance
    
    try:
        db = connect("ATMdatabase.db")
        cursor = db.cursor()
        cursor.execute("UPDATE users SET balance = ? WHERE card_id = ?", (currentBalance, card_id,))
        db.commit()  # Commit the changes to the database
        print(f"\nDeposit successful. New balance: {currentBalance}")
    except Error as e:
        print(f"Database error: {e}")
    finally:
        db.close()

def transfer(card_id: str):
    """Handle fund transfer between the logged-in user and another user."""
    currentBalance = checkBalance(current_user)  # Get the current balance of the user
    print(f"\nBalance: {currentBalance}")
    
    targetCardId = input("Enter the target card ID: ")
    
    try:
        db = connect("ATMdatabase.db")
        cursor = db.cursor()
        cursor.execute("SELECT card_id FROM users WHERE card_id = ?", (targetCardId,))
        findUser = cursor.fetchone()
        
        if not findUser:  # If the target card ID doesn't exist, print error
            print("Can't find card id!")
        else:
            transferAmount = int(input("Enter amount to transfer: "))
            
            if transferAmount > currentBalance:  # Ensure sufficient funds for transfer
                print("Insufficient funds.")
            else:
                currentBalance -= transferAmount  # Deduct the transfer amount from the user's balance
                
                targetBalance = checkBalance(targetCardId)  # Get the current balance of the target account
                targetBalance += transferAmount  # Add the transfer amount to the target account balance
                
                # Update both user's and target's balance in the database
                cursor.execute("UPDATE users SET balance = ? WHERE card_id = ?", (targetBalance, targetCardId,))
                db.commit()
                
                cursor.execute("UPDATE users SET balance = ? WHERE card_id = ?", (currentBalance, card_id,))
                db.commit()
                
                print(f"Transfer successful. Your new balance: {currentBalance}")
                print(f"Target account new balance: {targetBalance}")
        
    except Error as e:
        print(f"Database error: {e}")
    finally:
        db.close()

def main():
    """Main menu for the ATM system. Handles login and account operations."""
    if not login_status:  # If user is not logged in, show login/register options
        print("Options:\n1. Login\n2. Register")
        optionSelected = input("Select an option: ")
        
        match optionSelected:
            case "1":
                login()
            case "2":
                register()
            case _:
                print("Invalid input!")
                
    if login_status:  # If user is logged in, show the main menu with account options
        while True:
            print("\nMenu: \n1. Check Balance\n2. Withdraw\n3. Deposit\n4. Transfer\n5. Logout\n")
            selectedMenu = input("Select an option: ")
            
            match selectedMenu:
                case "1":
                    print(f"\nBalance: {checkBalance(current_user)}")
                case "2":
                    withdraw(current_user)
                case "3":
                    deposit(current_user)
                case "4":
                    transfer(current_user)
                case "5":
                    endProgram = input("Confirm logout? (y/n): ").lower()
                    if endProgram == "y":  # Confirm logout action
                        break
                    pass
                case _:
                    print("Invalid input!")

if __name__ == "__main__":
    main()
