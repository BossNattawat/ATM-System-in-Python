# ATM Management System

This project is a simple command-line ATM Management System written in Python. It allows users to perform basic banking operations such as registration, login, checking balance, withdrawing funds, depositing money, and transferring funds. The data is stored in an SQLite database (`ATMdatabase.db`).

## Features

1. **User Registration**:
   - Users can register with their name, an 8-digit card ID, and a password.
   - Passwords are hashed using SHA256 before being stored for security.

2. **User Login**:
   - Users log in using their card ID and password.
   - The system verifies credentials and tracks login status.

3. **Account Operations**:
   - **Check Balance**: View the current balance of the logged-in user.
   - **Withdraw Funds**: Withdraw money from the account, ensuring sufficient funds.
   - **Deposit Money**: Add money to the account.
   - **Transfer Funds**: Transfer money to another user by specifying their card ID.

4. **Security**:
   - Passwords are stored securely using SHA256 hashing.
   - Only valid card IDs and user credentials are processed.

5. **Data Storage**:
   - User data (name, card ID, password, and balance) is stored in an SQLite database (`ATMdatabase.db`).

## How It Works

1. **Registering a New User**:
   - Users must enter a valid name (alphabets and spaces only), an 8-digit card ID, and a password (minimum 6 characters).
   - The system checks for existing usernames or card IDs to prevent duplicates.
   - On successful registration, the user is automatically logged in.

2. **Logging In**:
   - Users provide their card ID and password.
   - The system retrieves the user record from the database and compares the provided password (hashed) with the stored hash.

3. **Performing Transactions**:
   - After login, users can access the main menu to perform operations:
     - **Check Balance**: Fetch and display the account balance from the database.
     - **Withdraw**: Deduct the specified amount from the user's balance, ensuring sufficient funds.
     - **Deposit**: Add the specified amount to the user's balance.
     - **Transfer**: Deduct the transfer amount from the user's balance and add it to the target user's account.

4. **Logout**:
   - Users can logout by confirming their choice.

## Database Structure

The database (`ATMdatabase.db`) contains a table named `users` with the following schema:

| Column      | Type    | Description                            |
|-------------|---------|----------------------------------------|
| `id`        | INTEGER | Primary key, auto-incremented          |
| `name`      | TEXT    | User's name                            |
| `card_id`   | TEXT    | 8-digit unique identifier for the user |
| `password`  | TEXT    | Hashed password                        |
| `balance`   | INTEGER | Account balance (default: 1000)           |

## Usage

1. **Run the program**

   ```python
   python3 ATM.py
   ```

2. **Follow the interactive prompts:**
    - **Select an option (1 for Login or 2 for Register).**

        - Login: Enter your card ID and Password.

        - Register: Enter your name, card ID, password, confirm pass.

    - **After login Select an option:**
        - 1 for check balance
        
        - 2 for withdraw

            - Enter amount to withdraw

        - 3 for deposit

            - Enter amount to deposit

        - 4 for transfer

            - Enter the target card ID

            - Enter amount to transfer

        - 5 for logout

            - Confirm logout? (y/n)

---

### License

This project is licensed under the MIT License. Modify and distribute freely with proper attribution.