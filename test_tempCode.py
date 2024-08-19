import requests

# Base URL of the Flask Server
base_url = "http://127.0.0.1:5001"

# Function to Generate the Verification Code
def generate_code(email):
    url = f"{base_url}/generate-code"
    data = {"email": email}
    try:
        response = requests.post(url, json=data)
        response.raise_for_status()  # Triggers an Error if the Status Code is Not 200
        print(f"Verification Code Sent To {email}.")
    except requests.exceptions.HTTPError as http_err:
        print(f"HTTP Error Occurred While Generating Code: {http_err}")
        print(f"Server Response: {response.text}")
    except Exception as err:
        print(f"Error in Code Generation: {err}")

# Function to Verify the Verification Code
def verify_code(email, code):
    url = f"{base_url}/verify-code"
    data = {"email": email, "code": code}
    try:
        response = requests.post(url, json=data)
        response.raise_for_status()  # Triggers an Error if the Status Code is Not 200
        print("Valid Verification Code!")
    except requests.exceptions.HTTPError as http_err:
        print(f"HTTP Error Occurred While Verifying Code: {http_err}")
        print(f"Server Response: {response.text}")
    except Exception as err:
        print(f"Error During Code Verification: {err}")

def main():
    # Email to Receive the Code
    test_email = "daniucs@gmail.com"

    # 1. Generate the Verification Code
    generate_code(test_email)

    # Simulates Receiving the Code via Email (For Testing Purposes)
    # In a Real Scenario, the Code Would Be Read from the User's Email
    received_code = input("Enter the Verification Code Received by Email: ")

    # 2. Validate the Verification Code
    verify_code(test_email, received_code)

if __name__ == "__main__":
    main()
