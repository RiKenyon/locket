import sqlite3
from tabulate import tabulate

path = "locket.db"
def connect():
    return sqlite3.connect(path)


#intro access
CREATE_USERS_TABLE = "CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY, username TEXT, password TEXT, fname TEXT, lname TEXT);"
CHECK_USER = "SELECT * FROM users WHERE username = ? AND password = ?"
INSERT_USER = "INSERT INTO users (username, password, fname, lname) VALUES (?, ?, ?, ?);"
CHECK_DUPICATES = "SELECT COUNT(*) FROM users WHERE username = ?;"


def create_tables(connection):
    with connection:
        connection.execute(CREATE_USERS_TABLE)


def check_user(connection, username, password):
    with connection:
        cursor = connection.execute(CHECK_USER, (username, password))
        user = cursor.fetchone()
        if user:
            return username
        

    
def add_user(connection, username, password, fname, lname):
    with connection:
        connection.execute(INSERT_USER, (username, password, fname, lname))

def user_duplicate(connection, username):
    with connection:
        cursor= connection.execute(CHECK_DUPICATES, (username,))
        count = cursor.fetchone()
        return count[0] > 0 if count else False

CREATE_ACCOUNTS_TABLE = "CREATE TABLE IF NOT EXISTS user_accounts (id INTEGER PRIMARY KEY, account_name TEXT, account_username TEXT, account_password TEXT, user_id INTEGER, FOREIGN KEY (user_id) REFERENCES users(id));"
GET_PASSWORD_BY_ACCOUNT = "SELECT user_accounts.account_name, user_accounts.account_username, user_accounts.account_password FROM user_accounts JOIN users ON user_accounts.user_id = users.id WHERE users.username = ? AND user_accounts.account_name = ?"
DISPLAY_ALL_ACCOUNTS = "SELECT user_accounts.account_name, user_accounts.account_username, user_accounts.account_password FROM user_accounts JOIN users ON user_accounts.user_id = users.id WHERE users.username = ?" 
ADDING_ACOUNTS = "INSERT INTO user_accounts (account_name, account_username, account_password, user_id) VALUES (?, ?, ?, ?)"
USER_ID_CHECK = "SELECT id FROM users WHERE username = ?"
DELETE_ACCOUNT = "DELETE FROM user_accounts WHERE account_name = ? AND user_id = ?"
UPDATE_ACCOUNT = "UPDATE user_accounts SET account_username = ?, account_password = ? WHERE account_name = ? AND user_id = ?"
def create_tables_account(connection):
    with connection:
        connection.execute(CREATE_ACCOUNTS_TABLE)

def check_id(connection, username):
    with connection:
        cur =  connection.execute(USER_ID_CHECK, (username,))
        result = cur.fetchone()
        return result[0] if result else None
        

def add_accounts(connection, account_name, account_username, account_password, user_id):
    with connection:
        connection.execute(ADDING_ACOUNTS, (account_name, account_username, account_password, user_id))

def show_all_accounts(connection, username):
    with connection:
        cursor = connection.execute(DISPLAY_ALL_ACCOUNTS, (username,))
        accounts = cursor.fetchall()

        if accounts:
            print(f"Acounts for {username}:\n")
            print(tabulate(accounts, headers= ["ACCOUNT NAME","ACCOUNT USERNAME","ACCOUNT PASSWORD"], tablefmt="fancy_grid"))
        else:
            print("No entries yet")

def find_accounts(connection, username, account_name):
    with connection:
        cursor = connection.execute(GET_PASSWORD_BY_ACCOUNT, (username, account_name))
        accounts = cursor.fetchall()
        if not accounts:
            print("\nnothing found\n")
        print(tabulate(accounts, headers= ["ACCOUNT NAME","ACCOUNT USERNAME","ACCOUNT PASSWORD"], tablefmt="fancy_grid"))


def delete_accounts(connection, account_name, user_id):
    with connection:
        connection.execute(DELETE_ACCOUNT, (account_name, user_id))

def update_account(connection, account_name, account_username, account_password, user_id):
    with connection:
        connection.execute(UPDATE_ACCOUNT, (account_username, account_password, account_name, user_id))