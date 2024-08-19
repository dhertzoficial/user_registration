import requests

API_URL = 'http://127.0.0.1:5000'

def check_json_structure():
    response = requests.get(f'{API_URL}/users')
    if response.status_code == 200:
        users = response.json()
        print(users)  # Print the JSON Structure
    else:
        print(f"Failed to fetch users: {response.status_code}")

check_json_structure()
