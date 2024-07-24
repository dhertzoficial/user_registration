import requests
import pwinput # essa biblioteca precisa ser instalada e tem objetivo de mostrar asteriscos no terminal ao digitar password
import re # regra de caracteres para passwords

#STATUS CODES: 0 == inactive; 1 == pending; 2 == active

API_URL = 'http://127.0.0.1:5000'

def show_users():
    response = requests.get(f'{API_URL}/users')
    if response.status_code == 200:
        users = response.json()
        
        # USER HEADER
        print(f"{'ID':<4} | {'EMAIL':<30} | {'PASSWORD':<12} | {'NAME':<12} | {'STATUS':<10}")
        print("-"*70)            

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

            print(f"{id:<4} | {email:<30} | {password:<12} | {name:<12} | {color}{status_string:<10}{RESET}")
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

def add_user():
    # REGRA PARA TER @ NO EMAIL
    while True:
        email = input("\nPlease, enter your email: ").lower()
        if "@" in email:
            break
        else:
            print("Email invalid, please try again.")

    # REGRA CARACTERES PASSWORD
    while True:
        try:
            password = pwinput.pwinput('''\nPlease, enter your password: 
                                       The length must be between 8 and 12 caracters,
                                       Also must contains at least une number, one special caracter,
                                       one upper and one lower case letter: ''', mask='*')
            validate_password(password)
            break
        except ValueError as e:
            print(e)
            
    name = input("\nPlease, enter your name: ").upper()
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
        print(f"\nError creating user {name}")
    

def delete_user():
    
    # ANSI CODE FOR COLOR
    RED = '\033[91m'
    RESET = '\033[0m'
    
    user_id = int(input("\nPlease, enter the user ID do be deleted: "))
    confirmation = input(f"\n{RED}Are you sure you want to delete the user id'{user_id}'?  (y/n):  {RESET}").lower()
    if confirmation != 'y':
        print(f"\nOperação abortada")
    else:
        response = requests.delete(f'{API_URL}/users/{user_id}')
        if response.status_code == 200:
            print(f"\nUser {user_id} deleted successfully")
        else:
            print(f"\nError deleting user {user_id}")

def update_user():
    user_id = int(input("\nPlease, enter the user ID to be updated: "))
    email = input("\nPlease, enter the new e-mail: ").lower()
    name = input("\nPlease, enter new name: ").upper()
    user_data = {
        'email': email,
        'name': name
    }
    response = requests.put(f'{API_URL}/users/{user_id}', json=user_data)
    if response.status_code == 200:
        print(f"\nUser {user_id} updated successfully")
    else:
        print(f"\nError updating user {user_id}")

def troca_senha():
    user_id = int(input("\nPlease, enter the user ID to update the password: "))
    password = input("\nPlease, enter the new password: ")
    user_data = {
        'password': password,
    }
    response = requests.put(f'{API_URL}/users/{user_id}', json=user_data)
    if response.status_code == 200:
        print(f"\nUser {user_id} password updated successfully")
    else:
        print(f"\nError updating user {user_id}")   
    

def altera_status():
    user_id = int(input("\nPlease, enter the user ID to update the status: "))
    status = input("\nPlease, enter the new status (0 == inactive, 1 == pending, 2 == active): ")
    user_data = {
        'status': status,
    }
    response = requests.put(f'{API_URL}/users/{user_id}', json=user_data)
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


    # verificar se ao cadastrar email ou alterar email, ja nao existe cadastro com o mesmo email
    # verificacao em duas etapas para login - usar servico sendgrid
    # funcao exclusiva para troca de senha
    # funcao exclusiva para inativar um id

# IMPLEMENTAÇÕES OK
  # email com @ - ok
  # função deletar, vai excluir usuário caso o mesmo já esteja inativo
  # Passwords com asterisco no terminal
  # tamanho maximo de passwords
  # emails em lower, nomes em upper
  # colocar regra na senha. pelo menos um caracter especial, um upper, um lowe e um numero (biblioteca re)
  # conceito server / client usando API

