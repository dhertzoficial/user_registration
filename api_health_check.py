import requests

API_URL = 'http://127.0.0.1:5000'

def health_check():
    response = requests.get(f'{API_URL}/health')
    if response.status_code == 200:
        print(response.json()['status'])
    else:
        print("Failed to connect to the database")

def main():
    health_check()

if __name__ == "__main__":
    main()