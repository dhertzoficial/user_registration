import requests

API_URL = 'http://127.0.0.1:5000'

def user_exists(user_id):
    response = requests.get(f'{API_URL}/users')
    if response.status_code == 200:
        users = response.json()
        for user in users:
            if user[0] == user_id:  # Verifica se o ID do usuário corresponde ao ID procurado
                return True
    return False

def test_user_exists(user_id):
    if user_exists(user_id):
        print(f"User with ID {user_id} exists.")
    else:
        print(f"User with ID {user_id} does not exist.")

if __name__ == '__main__':
    user_id_to_test = int(input("Enter the user ID to check: "))
    test_user_exists(user_id_to_test)
