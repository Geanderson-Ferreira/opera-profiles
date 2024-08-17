import requests

def log():
    pass

def get_address(cep):
    response = requests.get(f"https://viacep.com.br/ws/{cep}/json/")
    if response.status_code == 200:
        return response.json()
    else:
        print("Function get_address_from_cep response <> 200.")
        return False