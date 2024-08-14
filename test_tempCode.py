import requests

# URL base do servidor Flask
base_url = "http://127.0.0.1:5001"

# Função para gerar o código de verificação
def generate_code(email):
    url = f"{base_url}/generate-code"
    data = {"email": email}
    try:
        response = requests.post(url, json=data)
        response.raise_for_status()  # Levanta um erro se o status não for 200
        print(f"Código de verificação enviado para {email}.")
    except requests.exceptions.HTTPError as http_err:
        print(f"Erro HTTP ao gerar código: {http_err}")
        print(f"Resposta do servidor: {response.text}")
    except Exception as err:
        print(f"Erro ao gerar código: {err}")

# Função para verificar o código de verificação
def verify_code(email, code):
    url = f"{base_url}/verify-code"
    data = {"email": email, "code": code}
    try:
        response = requests.post(url, json=data)
        response.raise_for_status()  # Levanta um erro se o status não for 200
        print("Código de verificação válido!")
    except requests.exceptions.HTTPError as http_err:
        print(f"Erro HTTP ao verificar código: {http_err}")
        print(f"Resposta do servidor: {response.text}")
    except Exception as err:
        print(f"Erro ao verificar código: {err}")

def main():
    # Email para o qual o código será enviado
    test_email = "daniucs@gmail.com"

    # 1. Gerar o código de verificação
    generate_code(test_email)

    # Simula o recebimento do código por email (para fins de teste)
    # Em um cenário real, o código seria lido do email do usuário
    received_code = input("Insira o código de verificação recebido por email: ")

    # 2. Verificar o código de verificação
    verify_code(test_email, received_code)

if __name__ == "__main__":
    main()
