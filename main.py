import sqlite3
import pwinput # essa biblioteca precisa ser instalada e tem objetivo de mostrar asteriscos no terminal ao digitar password

def to_connect():
    connection = sqlite3.connect("database.db")
    cursor = connection.cursor()
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS users(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    email TEXT NOT NULL,
    password TEXT NOT NULL,
    name TEXT NOT NULL,
    status INTEGER NOT NULL)
''')
    connection.commit()
    return connection, cursor

def show_users():
    connection, cursor = to_connect() # abrindo conexao
    cursor.execute('SELECT * FROM users ORDER BY id')# selecionando toda tabela e ordenando
    users = cursor.fetchall() # opening cursor
    print("")
    
    # users header
    print(f"{'ID':<4} | {'EMAIL':<15} | {'PASSWORD':<12} | {'NAME':<12} | {'STATUS':<10}")
    print("-"*70)

    # ANSI COLOR
    RED = '\033[91m'
    GREEN = '\033[92m'
    RESET = '\033[0m'

    for user in users: 
        id, email, password, name, status = user
        status = int(status)
        color = GREEN if status == 1 else RED
        status_string = "active" if status == 1 else "Inactive"
        print(f"{id:<4} | {email:<15} | {password:<12} | {name:<12} | {color}{status_string:<10}{RESET}")
        print("")
    
    connection.close()

def add_user():
    connection, cursor = to_connect() # abrindo conexao
    email = input("\n Please, enter your email: ")
    
    while True:
        password = pwinput.pwinput(" Please, enter your password: The length must be between 8 and 12 caracters: ", mask='*')
        if len(password) >= 8 and len(password) <= 12:
            break
        else:
            print("Tente novamente. Verifique a quantidade minima e maxima de caracteres aceitos")
    name = input(" Please, enter your name: ")
    status = 1 # status default - active
    cursor.execute('''
                   INSERT INTO users
                   (email, password, name, status) 
                   VALUES(?, ?, ?, ?)
                   ''', (email, password, name, status))
    connection.commit()
    connection.close()
    print("User added successfully!")

def delete_user():
    connection, cursor = to_connect()
    user_id = int(input("\nPlease, enter the user ID do be deleted: "))
    
    # ANSI CODE FOR COLOR
    YELLOW = '\033[93m'
    RESET = '\033[0m'

    #Take the email
    cursor.execute('SELECT email FROM users WHERE id = ?', (user_id,))
    user = cursor.fetchone()

    if user:
        email = user[0]

    confirmation = input(f"\n{YELLOW}Are you sure you want to delete the user '{email}'?  (y/n) {RESET}").lower()
    if confirmation == 'y':
        status = 0
        cursor.execute('''
                    UPDATE users
                    SET status = ?
                    WHERE id = ?
                    ''', (status, user_id))
        connection.commit()
        print("\nuser successfully deactivated")
    else:
        print("\nExclusion cancelled")

    connection.close()

def update_user():
    connection, cursor = to_connect()
    user_id = int(input("\nPlease, enter the user ID to be updated: "))
    
    what_update = (int(input("\nO que voce gostaria de alterar? \n- 1 - email \n- 2 - nome \n- 3 - password \n- 4 - status \n- 5 - leave \n Digite aqui: " )))
    
    if what_update == 1:
        email = input("Please, enter new email: ")
        cursor.execute('''
                        UPDATE users
                        SET email = ?
                        WHERE id = ?
                        ''', (email, user_id))
    elif what_update == 2:
        name = input("Please, enter new name: ")
        cursor.execute('''
                        UPDATE users
                        SET name = ?
                        WHERE id = ?
                        ''', (name, user_id))
    elif what_update == 3:
        while True:
            password = input(" Please, enter your password: The length must be between 8 and 12 caracters ")
            if len(password) >= 8 and len(password) <= 12:
                break
            else:
                print("Tente novamente. Verifique a quantidade minima e maxima de caracteres aceitos")
        cursor.execute('''
                        UPDATE users
                        SET password = ?
                        WHERE id = ?
                        ''', (password, user_id))
    elif what_update == 4:
        status = int(input('Please, enter new status: \n 0 - inativo \n 1 - ativo \n Digite aqui:  '))
        cursor.execute('''
                        UPDATE users
                        SET status = ?
                        WHERE id = ?
                        ''', (status, user_id))
    elif what_update == 5:
        main()
    else:
        print("Invalid option")

    
    connection.commit()
    connection.close()
    print("\nuser successfully updated")


def main():
    to_connect()
    while True:
        print("\nMenu:")
        print("1 - Show users")
        print("2 - Add user")
        print("3 - Delete user")
        print("4 - Update user")
        print("5 - Quit")

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
            break
        else:
            print("Invalid option")
    


if __name__ == "__main__":
    main()


    # email com @
    # colocar regra na senha. pelo menos um caracter especial, um upper, um lowe e um numero (biblioteca re)
    # lembrando que esse programa vai ser um programa de login. entao provavalmente eu vou precisar
    # usar um outro arquivo py que vai usar o banco de dados para validar entrada
    # verificar se ao cadastrar email ou alterar email, ja nao existe cadastro com o mesmo email
    # email para validar email cadastrado. clicar no link para ativar usuario. talvez novo status. usuario pendente
    # verificacao em duas etapas para login - usar servico sendgrid

