import requests
from os import environ
from dotenv import load_dotenv
import json

load_dotenv()

def get_profiles_by_ids(ids:list, hotel, token):

    limit = 190
    all_profiles = []

    for i in range(0, len(ids), limit):

        ids_to_request = ids[i:i + limit]

        url = f"{environ['APIGW_URL']}/crm/v1/profilesByIds"

        payload = {}
        headers = {
        'x-hotelid': hotel,
        'x-app-key': environ['APP_KEY'],
        'Authorization': f'Bearer {token}'
        }

        params = {
            "profileIds": ids_to_request,
        "fetchInstructions": ["Address", "Comment", "Communication", "Profile"]
        }

        response = requests.request("GET", url, headers=headers, data=payload, params=params)

        if response.status_code == 200:
            all_profiles.extend(response.json()['profiles'].get('profileInfo',[]))
        else:
            print(response.text)
            return False
        
    return all_profiles

def update_profile_address(profile_id, address_info, hotel, token):

    """
    #Modelo address_info
    {
            "address": {
                "addressLine": [
                "3450 North Triumph Boulevard Suite 300",
                "",
                "",
                ""
                ],
                "cityName": "Lehi",
                "postalCode": "84043",
                "state": "UT",
                "country": {
                "value": "US"
                },
                "language": "E",
                "type": "HOME",
                "primaryInd": False
            },
            "type": "Address",
            "id": "45115"
            }
    """

    url = f"https://acc2-oc.hospitality-api.us-ashburn-1.ocs.oraclecloud.com/crm/v1/profiles/d{profile_id}"

    payload = json.dumps({
    "profileDetails": {
        "addresses": {
        "addressInfo": [
            address_info
        ]
        }
    },
    "profileIdList": [
        {
        "type": "Profile",
        "id": profile_id
        }
    ]
    })
    headers = {
    'Content-Type': 'application/json',
    'x-app-key': environ['APP_KEY'],
    'x-hotelid': hotel,
    'Authorization': f'Bearer {token}'
    }

    response = requests.request("PUT", url, headers=headers, data=payload)

    print(response.text)


class Profile:
    def __init__(self):
        pass

    def search_profiles(self, params: dict, hotel: str, token: str):


        url = f"{environ['APIGW_URL']}/crm/v1/profiles"

        payload = {}
        headers = {
        'x-app-key': environ['APP_KEY'],
        'x-hotelid': hotel,
        'Authorization': f'Bearer {token}'
        }

        response = requests.request("GET", url, headers=headers, data=payload, params=params)

        print(response.text)


