import requests

API_URL = 'http://127.0.0.1:5000'

def email_exists(email):
    response = requests.get(f'{API_URL}/users/email_exists?email={email}')
    return response.json()['exists']

def email_existence(email):
    if email_exists(email):
        print(f"The email {email} Exists in the Database.")
        return True
    else:
        print(f"The email {email} doesn't exists in the Database.")
        return False

def main():
    email = input("Enter the Email to Verify: ")
    email_existence(email)

if __name__ == "__main__":
    main()
