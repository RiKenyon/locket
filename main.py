
import database
import maskpass                                                                                                                             #<--- Password diplay"*"
import sys, subprocess
import random
import string


operating_sys = sys.platform 
connection = database.connect()

INTRO = """---LOCKET---

[1] Log In
[2] Sign Up
[3] Exit

Enter your required number here:
>>> """

MAIN_MENU = """---MAIN MENU---

[1] View All Accounts
[2] Add Account
[3] Search Account
[4] Log Out


Enter your required number here:
>>> """

EXIT = """Are you sure you want to log-out
[1] Yes
[2] No

Enter your required number here:
>>> """


def clear_screen():   
                                                                                                                          #<---Clears Terminal Display
    try:                                                                                                                                    #checks operating system
        if operating_sys == 'win32':                                                                                                        #win32 == windows
            subprocess.run('cls', shell=True)
        elif operating_sys == 'linux' or operating_sys == 'darwin':
            subprocess.run('clear', shell= True)                                                                                            #darwin == apple
    except:
        print("Encountered an error")
    

def log_in():#<---Checking access for login
    database.create_tables(connection)                                                                                                                              
    print("***LOGIN***")
    print("------------------")
    username = input("Enter Username: ").lower()
    password = maskpass.askpass(mask="*")   
    try:                                                                                                #display "*" when entering
        if database.check_user(connection, username, password):                                                                                         #!need db to check user!
            print("Login successful")
            user_access = username
            return user_access

        else:
            clear_screen()
            print("Invalid username or password")  
    except:
        print("Encountered an error")


def sign_up():                                                                                                                              #<--CREATES ACCOUNT
    database.create_tables(connection)                                                                                                   #creates a user tabel if it doesn't exsit               
    print("***Sign Up***")
    print("------------------")
    fname = input("Enter First Name: ").lower()
    lname = input("Enter Last Name: ").lower()
    username = input("Create Username: ").lower()
    if database.user_duplicate(connection, username):                                                                                    #it checkes if there is any duplicates
        clear_screen()                                                                                                                   #it will go back to the start of the function
        print("!Username already exist, try again!")
        sign_up()
    print("(Passwords needs to be 6 or more characters long )")                                                                          
    password = maskpass.askpass(prompt="Create Password: ", mask="*")                                                                    #display "*" when entering
    confirm_password = maskpass.askpass(prompt="Confirm Password: ", mask="*")                                                           #need db to start
    if password != confirm_password:
        print("Passwords do not match, try again")                                                                                       #VV password check VV
        sign_up()                                                                                                                        #vv                vv
    elif len(password) < 5:
        print("Password isn't long enough, try again")
        sign_up()                                                           
    else:
        clear_screen()
        database.add_user(connection, username,password,fname,lname)                                                                    #account created and submited to the database
        print("!User created!")
        
            
            
def view_all(username):                                                                                                                 #<---DISPLAYS ALL VALUES IN THE DATABASE
    print("***VIEW ALL***")                                                                                                             
    print("------------------")
    database.show_all_accounts(connection, username)                                                                                    #collects everything
    print(input("Press Enter to Exit"))

def find_account(username):
    print("**SEARCH ACCOUNT**")
    print("------------------")
    account_name = input("\nEnter Account Name:\n>>>").lower()
    database.find_accounts(connection, username, account_name)
    user_input = input("""[1] Update  [2] Search Again  [3] Delete  [4] Exit\n\nEnter here: """)
    if user_input == "1":
        print("**UPDATE**")
        print("------------------")
        print("ACCOUNT NAME: " + account_name + "\n\n")
        account_username = input("Update Account Username: ").lower()
        user_input= input("""
Would you like to generate a password?
          
[1]Yes
[2]No

Enter your required number here: """)
        if user_input == "1":
            clear_screen()
            account_password = generate_password(password='')
        elif user_input =="2":
            account_password = input("Enter New Account Password: ")

            if database.update_account(connection, account_name, account_username,account_password, database.check_id(connection, username)):
                clear_screen()
            print("Successfully Updated!")

    elif user_input == "2":
        clear_screen()
        find_account(username)
        
    elif user_input == "3":
        user_input = input("""Are you sure you want to delete this?

[1] Yes
[2] No
    
Enter your required number here:
>>> """)
    if user_input == "1":
        database.delete_accounts(connection, account_name, database.check_id(connection, username))
        clear_screen()
    elif user_input == "4":
        clear_screen()
    

def add_account(username):
    database.create_tables_account(connection)
    print("***ADD ACCOUNT***")
    print("------------------")
    account_name = input("Enter Account Name: ").lower()
    account_username = input("Enter Account Username: ").lower()
    user_input= input("""
Would you like to generate a password?
          
[1]Yes
[2]No

Enter here: """)
    if user_input == "1":
        clear_screen()
        account_password = generate_password(password='')
    elif user_input =="2":
        account_password = input("Enter Account Password: ")
    if database.add_accounts(connection, account_name, account_username, account_password, database.check_id(connection, username)):
        clear_screen()
        print("Succefully added")
    

def generate_password(password):
    print("***PASSWORD GEN***")
    print("------------------")
    char = int(input("How many letters: "))
    num = int(input("How many numbers: "))
    spec = int(input("How many special characters: "))
    length = char + num + spec
    
    while True:

        password = ''.join([random.choice([random.choice(string.ascii_letters) for x in range(char)] + [random.choice(string.digits) for x in range(num)] + [random.choice(string.punctuation) for x in range(spec)]) for x in range(length)])
        

        print(f"\nYour password is: {password}")
        user_input = input("""
Does this password work for you?
                       
[1]Yes
[2]No

Enter here: """)
        if user_input == "1":
            return password
        elif user_input == "2":
            print("***ADD ACCOUNT***")
            print("------------------")
            

            
    


def main_menu(username):
    clear_screen()
    while True:
        user_input = input(MAIN_MENU)
        
        if user_input == "1":
            clear_screen()
            view_all(username)
            clear_screen()

        elif user_input == "2":
            clear_screen()
            add_account(username)
            clear_screen()
            
        
        elif user_input == "3":
            clear_screen()
            find_account(username)
            clear_screen()
        
        
        elif user_input == "4":
            clear_screen()
            user_input = input(EXIT)
            if user_input == "1":
                clear_screen()
                return True
            elif user_input == "2":
                clear_screen()
        
        
        else:
            print("Invalid entry")


    
def main():
    clear_screen()
    while (user_input := input(INTRO)) != "3":
        clear_screen()
        if user_input == "1":
            clear_screen()
            username = log_in()
            if username:
                main_menu(username)

        elif user_input == "2":
            clear_screen()
            sign_up()
            
        elif user_input == "3":
            clear_screen()
        else:
            print("Invalid entry")
    clear_screen() 
    print("Thank you for using Locket")

main()