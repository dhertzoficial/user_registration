import requests

API_URL = 'http://127.0.0.1:5000'

def id_exists(user_id):
    response = requests.get(f'{API_URL}/users/exists?id={user_id}')
    return response.json()['exists']

def id_existence(user_id):
    if id_exists(user_id):
        print(f"O usuário com ID {user_id} existe no banco de dados.")
        return True
    else:
        print(f"O usuário com ID {user_id} não existe no banco de dados.")
        return False

def main():
    user_id = input("Digite o ID do usuário para verificar: ")
    id_existence(user_id)

if __name__ == "__main__":
    main()
