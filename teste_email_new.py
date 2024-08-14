import requests

API_URL = 'http://127.0.0.1:5000'

def email_exists(email):
    response = requests.get(f'{API_URL}/users/email_exists?email={email}')
    return response.json()['exists']

def email_existence(email):
    if email_exists(email):
        print(f"O email: {email} existe no banco de dados.")
        return True
    else:
        print(f"O email {email} não existe no banco de dados.")
        return False

def main():
    email = input("Digite o email para verificar: ")
    email_existence(email)

if __name__ == "__main__":
    main()
