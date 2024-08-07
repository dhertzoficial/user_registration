import requests

API_URL = 'http://127.0.0.1:5000'

def email_exists(email):
    response = requests.get(f'{API_URL}/users')
    if response.status_code == 200:
        users = response.json()
        for user in users:
            if user[1] == email:  # Verifica se o email já existe no banco de dados
                return True
    return False

def main():
    email = input("Please, enter the email to check if it exists: ").lower()
    if email_exists(email):
        print(f"Email {email} already exists in the database.")
    else:
        print(f"Email {email} does not exist in the database.")

if __name__ == "__main__":
    main()
