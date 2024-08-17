import requests
import json
from os import environ
from dotenv import load_dotenv

load_dotenv()

def check_token(hotel, token):

    url = f"{environ['APIGW_URL']}/bof/v1/hotels/{hotel}/businessDate"

    payload = ""
    headers = {
    'Content-Type': 'application/json',
    'x-hotelid': hotel,
    'x-app-key': environ['APP_KEY'],
    'Authorization': f'Bearer {token}'
    }

    response = requests.request("GET", url, headers=headers, data=payload)

    if response.status_code == 200:
        return {'token_is_valid':True, 'info': 'Token Valido'}
    else:
        return {'token_is_valid': False, 'info': response.text}
        
