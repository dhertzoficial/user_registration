import time
import requests
import pwinput # essa biblioteca precisa ser instalada e tem objetivo de mostrar asteriscos no terminal ao digitar password
import re # regra de caracteres para passwords

#STATUS CODES: 0 == inactive; 1 == pending; 2 == active

API_URL = 'http://127.0.0.1:5000'


def user_exists(user_id):
    pass

def esc_to_menu():
    visual_effect("Returning to menu")
    main()

def visual_effect(message="Carregando", duration=10):
    print(message, end="")
    for _ in range (duration):
        print(".", end="", flush=True)
        time.sleep(0.1)
    print("Ok")

def show_users():
    response = requests.get(f'{API_URL}/users')
    if response.status_code == 200:
        users = response.json()
        
        visual_effect("\nShowing users")

        # USER HEADER
        print(f"\n{'ID':<4} | {'EMAIL':<30} | {'PASSWORD':<12} | {'NAME':<30} | {'STATUS':<10}")
        print("-"*100)            

        # ANSI COLOR
        RED = '\033[91m'
        GREEN = '\033[92m'
        YELLOW = '\033[93m'
        RESET = '\033[0m'

        

        for user in users: 
            id, email, password, name, status = user
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

            
            print(f"{id:<4} | {email:<30} | {password:<12} | {name:<30} | {color}{status_string:<10}{RESET}")
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
            visual_effect("Conferindo requisitos de senha")
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
            
        visual_effect("Conferindo requisitos de emails")
        # regra para conter arroba no email
        if "@" not in email:
            print("Error: Email invalid. No @.")
            continue
    
        # regra para conter ponto no email
        if "." not in email:
            print("Error: Email invalid. No dot.")
            continue

        if len(email) < 8:
            print("Error: Email invalid. Too short.")
            continue

        email_confirm = input("\nPlease, confirm your email (type ESC to return to main menu): ").lower()
        if email_confirm == "esc":
            visual_effect("\nMain menu selected ")
            main()
    
        visual_effect("Conferindo igualdade de emails")
        if email == email_confirm:
            return email
        else:
            print("Emails do not match. Please try again.")

def add_user():
 
    email = check_email()

    # REGRA CARACTERES PASSWORD
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

    confirmation = input(f"\n{RED}Are you sure you want to delete the user id'{user_id}'?  (y/n):  {RESET}").lower()
    if confirmation != 'y':
        print(f"\nOperação abortada")
    else:
        response = requests.delete(f'{API_URL}/users/{user_id}')
        visual_effect("\nContating database",duration=15)
        if response.status_code == 200:
            print(f"\nUser {user_id} deleted successfully")
        else:
            print(f"\nError deleting user {user_id}")

def update_user():
    user_id = (input("\nPlease, enter the user ID to be updated (type esc to go to main menu): "))
    if user_id.lower() == "esc":
        main()
    user_id = int(user_id)
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
    else:
        print(f"\nError updating user {user_id}")

def troca_senha():
    user_id = (input("\nPlease, enter the user ID to update the password (type esc to quit): "))
    if user_id.lower() == "esc":
        main()
    user_id = int(user_id)
    password = get_valid_password()
    user_data = {
        'password': password,
    }
    response = requests.put(f'{API_URL}/users/{user_id}', json=user_data)
    visual_effect("\nContating database",duration=15)
    if response.status_code == 200:
        print(f"\nUser {user_id} password updated successfully")
    else:
        print(f"\nError updating user {user_id}")   
    

def altera_status():
    user_id = (input("\nPlease, enter the user ID to update the status (type esc to quit): "))
    if user_id.lower() == "esc":
        main()
    user_id = int(user_id)
    status = input("\nPlease, enter the new status (0 == inactive, 1 == pending, 2 == active): ")
    user_data = {
        'status': status,
    }
    response = requests.put(f'{API_URL}/users/{user_id}', json=user_data)
    visual_effect("\nContating database",duration=15)
    if response.status_code == 200:
        print(f"\nUser {user_id} status updated successfully")
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
            troca_senha()
        elif choose == "6":
            altera_status()
        elif choose == "9":
            break
        else:
            print("Invalid option")
    


if __name__ == "__main__":
    main()


