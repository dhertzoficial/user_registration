import time
import requests
import pwinput # This library needs to be installed and the goal is to show the * in the terminal when something is typed
import re # password requirements

#STATUS CODES: 0 == inactive; 1 == pending; 2 == active

API_URL = 'http://127.0.0.1:5000'
GENERATING_CODE = 'http://127.0.0.1:5001/generate-code'
VERIFICATION_CODE = 'http://127.0.0.1:5001/verify-code'  


# ANSI CODE FOR COLOR
RED = '\033[91m'
RESET = '\033[0m'
GREEN = '\033[92m'
YELLOW = '\033[93m'

def email_exists(email):
    response = requests.get(f'{API_URL}/users/email_exists?email={email}')
    return response.json()['exists']

def email_existence(email):
    if email_exists(email):
        print(f"\n{RED}The email: {email} already exists in the database. Try another one.{RESET}")
        return True
    else:
        print(f"\n{GREEN}The email {email} doesn't exist in the database.{RESET}")
        return False

def id_exists(user_id):
    response = requests.get(f'{API_URL}/users/exists?id={user_id}')
    return response.json()['exists']

def id_existence(user_id):
    visual_effect("\nVerifying if user exists in database")
    if id_exists(user_id):
        print(f"\n{GREEN}The user with id: {user_id} already exists in the database.{RESET}")
        return True
    else:
        print(f"\n{RED}The user with id: {user_id} doesn't exist in the database.{RESET}")
        return False

def visual_effect(message="Processing", duration=10):
    print(message, end="")
    for _ in range (duration):
        print(".", end="", flush=True)
        time.sleep(0.1)
    print("Ok")

def esc_to_menu():
    visual_effect("Returning to menu")
    main()

def show_users():
    response = requests.get(f'{API_URL}/users')
    if response.status_code == 200:
        users = response.json()
        
        visual_effect("\nShowing users")

        # USER HEADER
        print(f"\n{'ID':<4} | {'EMAIL':<30} | {'NAME':<30} | {'STATUS':<10}")
        print("-"*100)            

        for user in users: 
            id, email, name, status = user["id"], user["email"], user["name"], user["status"]
            status = int(status)
            if status == 0:
                color = RED
                status_string = "Inactive"
            elif status == 1:
                color = YELLOW
                status_string = "Pending"
            elif status == 2:
                color = GREEN
                status_string = "Active"

            
            print(f"{id:<4} | {email:<30} | {name:<30} | {color}{status_string:<10}{RESET}")
            print("")
    else:
        print("No users found")

def validate_password(password):
    if len(password) < 8 or len(password) > 12:
        raise ValueError("The password must have between 8 and 12 caracters")
    if not re.search("[A-Z]", password):
        raise ValueError("The password must have at least one uppercase letter")
    if not re.search("[a-z]", password):
        raise ValueError("The password must have at least one lowercase letter")
    if not re.search("[0-9]", password):
        raise ValueError("The password must have at least one number")
    if not re.search("[!@#$%^&*(),.?:{}|<>]", password):
        raise ValueError("The password must have at least one special character")
    return True

def get_valid_password(prompt='''
                               \nPlease, enter your password: 
                                The length must be between 8 and 12 caracters,
                               Also must contains at least une number, one special caracter,
                               one upper and one lower case letter (Type esc to go to main menu): '''):
    while True:
        try:
            password = pwinput.pwinput(prompt, mask='*')
            if password.lower() == "esc":
                main()
            visual_effect("Checking Password Requirements")
            validate_password(password)
            password_confirm = pwinput.pwinput("\nPlease, confirm your password (Type esc to go to main menu): ")
            if password_confirm == "esc":
                main()
            if password == password_confirm:
                return password
            else:
                print("Passwords do not match. Please try again.")

        except ValueError as e:
            print(f"Invalid password: {e}")

def check_email():
    while True:
        email = input("\nPlease, enter your email (type ESC to return to main menu): ").lower()
        if email == "esc":
            visual_effect("\nMain menu selected ")
            main()

        visual_effect("\nChecking the email requirements")
        # Condition to Contain the @ Symbol in the Email
        if "@" not in email:
            print("Error: Email invalid. No @.")
            continue
    
        # Condition to Contain a Dot in the Emai
        if "." not in email:
            print("Error: Email invalid. No dot.")
            continue

        if len(email) < 8:
            print("Error: Email invalid. Too short.")
            continue

        if email_existence(email):
            add_user()

        email_confirm = input("\nPlease, confirm your email (type ESC to return to main menu): ").lower()
        if email_confirm == "esc":
            visual_effect("\nMain menu selected ")
            main()
    
        visual_effect("\nChecking Email Equality")
        if email == email_confirm:
            return email
        else:
            print("Emails do not match. Please try again.")

# Function to generate verification code
def generate_code(email):
    url = GENERATING_CODE
    data = {"email": email}
    try:
        response = requests.post(url, json=data)
        response.raise_for_status()  # raise an error if the status code is not 200
        print(f"Verification code sent to {email}.")
    except requests.exceptions.HTTPError as http_err:
        print(f"Error HTTP in generating code: {http_err}")
        print(f"Server response: {response.text}")
    except Exception as err:
        print(f"Error in generating code: {err}")

# function to verify the verification code
def verify_code(email, code):
    url = VERIFICATION_CODE
    data = {"email": email, "code": code}
    try:
        response = requests.post(url, json=data)
        response.raise_for_status()  # raise an error if the status code is not 200
        print("Verification code is valid!")
    except requests.exceptions.HTTPError as http_err:
        print(f"HTTP error during code verification: {http_err}")
        print(f"server response: {response.text}")
    except Exception as err:
        print(f"Code verification error: {err}")

def add_user():
 
    email = check_email()

    generate_code(email)

    code = input("\nEnter the code received by email: ")

    visual_effect("\nChecking the code on the server")

    verify_code(email,code)

    # checking password requirements
    password = get_valid_password()

    name = input("\nPlease, enter your name (Type esc do go to main menu): ").upper()
    if name == "ESC":
        main()
    status = 1 # status default - pending
    user_data = {
        'email': email,
        'password': password,
        'name': name,
        'status': status
    }
    response = requests.post(f'{API_URL}/users', json=user_data)
    if response.status_code == 200:
        print(f"\nUser {name} created successfully")
    else:
        print(f"\nError creating user {name}.")
    
def delete_user():
    
    # ANSI CODE FOR COLOR
    RED = '\033[91m'
    RESET = '\033[0m'
    
    user_id = (input("\nPlease, enter the user ID do be deleted (type esc to to main menu): "))
    if user_id.lower() == "esc":
        main()
    user_id = int(user_id)

    if not id_existence(user_id):
        print(f"\nTry again with a valide id.")
        delete_user()

    confirmation = input(f"\n{RED}Are you sure you want to delete the user id'{user_id}'?  (y/n):  {RESET}").lower()
    if confirmation != 'y':
        print(f"\nOperation canceled")
    else:
        response = requests.delete(f'{API_URL}/users/{user_id}')
        visual_effect("\nContating database",duration=15)
        if response.status_code == 200:
            print(f"\nUser {user_id} deleted successfully")
            main()
        else:
            print(f"\nError deleting user {user_id}")

def update_user():
    user_id = (input("\nPlease, enter the user ID to be updated (type esc to go to main menu): "))
    if user_id.lower() == "esc":
        main()
    user_id = int(user_id)
    
    if not id_existence(user_id):
        print(f"\nTry again with an existing ID.")
        update_user()
    
    email = check_email()
    name = input("\nPlease, enter new name (type esc do quit): ").upper()
    if name == "ESC":
        main()
    user_data = {
        'email': email,
        'name': name
    }
    response = requests.put(f'{API_URL}/users/{user_id}', json=user_data)
    visual_effect("\nContating database",duration=15)
    if response.status_code == 200:
        print(f"\nUser {user_id} updated successfully")
        main()
    else:
        print(f"\nError updating user {user_id}")

def change_password():
    user_id = (input("\nPlease, enter the user ID to update the password (type esc to quit): "))
    if user_id.lower() == "esc":
        main()
    user_id = int(user_id)

    if not id_existence(user_id):
        print(f"\nTry again with an existing ID.")
        change_password()

    password = get_valid_password()
    user_data = {
        'password': password,
    }
    response = requests.put(f'{API_URL}/users/{user_id}', json=user_data)
    visual_effect("\nContating database",duration=15)
    if response.status_code == 200:
        print(f"\nUser {user_id} password updated successfully")
        main()
    else:
        print(f"\nError updating user {user_id}")   
    
def update_status():
    user_id = (input("\nPlease, enter the user ID to update the status (type esc to quit): "))
    if user_id.lower() == "esc":
        main()
    user_id = int(user_id)

    if not id_existence(user_id):
        print(f"\nTry again with an existing ID.")
        update_status()

    status = input("\nPlease, enter the new status (0 == inactive, 1 == pending, 2 == active): ")
    user_data = {
        'status': status,
    }
    response = requests.put(f'{API_URL}/users/{user_id}', json=user_data)
    visual_effect("\nContating database",duration=15)
    if response.status_code == 200:
        print(f"\nUser {user_id} status updated successfully")
        main()
    else:
        print(f"\nError updating user {user_id}") 

def main():
    while True:
        print("\nMenu:")
        print("1 - Show users")
        print("2 - Add user")
        print("3 - Delete user")
        print("4 - Update user")
        print("5 - Change Password")
        print("6 - Altera Status")
        print("9 - Quit")

        choose = input("Please, enter the desired option: ")
        if choose == "1":
            show_users()
        elif choose == "2":
            add_user()
        elif choose == "3":
            delete_user()
        elif choose == "4":
            update_user()
        elif choose == "5":
            change_password()
        elif choose == "6":
            update_status()
        elif choose == "9":
            break
        else:
            print("Invalid option")

if __name__ == "__main__":
    main()


