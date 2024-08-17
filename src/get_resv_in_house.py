import requests
from dotenv import load_dotenv
from os import environ

load_dotenv()

def get_in_house(hotel, token):
    url = f"{environ['APIGW_URL']}/rsv/v1/hotels/{hotel}/reservations"
    headers = {
        'Content-Type': 'application/json',
        'x-hotelid': hotel,
        'x-app-key': environ['APP_KEY'],
        'Authorization': f'Bearer {token}'
    }
    
    all_reservations = []
    limit = 200
    offset = 0
    has_more = True
    
    while has_more:
        params = {
            'limit': limit,
            'offset': offset,
            'searchTypes': ['InHouse']
        }
        
        response = requests.get(url, headers=headers, params=params)
        
        if response.status_code == 200:
            data = response.json()
            reservations = data['reservations']['reservationInfo']
            all_reservations.extend(reservations)
            
            # Atualiza o offset e o has_more
            offset += limit
            has_more = data['reservations']['hasMore']
        else:
            return False
    
    return all_reservations