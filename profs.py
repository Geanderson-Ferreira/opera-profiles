from src.get_resv_in_house import get_in_house
from src.profiles import get_profiles_by_ids
from src.models_methods import get_active_rules_for_hotel
from src.models_methods import create_rule
from sqlalchemy import (
    create_engine, Column, String, Integer, Boolean,
    Text, ForeignKey, DateTime, func
)
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker
from os import environ
from dotenv import load_dotenv

def get_profile_data(hotel, token):

    engine = create_engine(environ['DB_CONNECTION'], echo=False)
    Session = sessionmaker(bind=engine)
    regras = get_active_rules_for_hotel(session=Session(),hotel_id=hotel)

    # Obter a lista de cadastros das reservas inHouse
    in_house_reservations = get_in_house(hotel, token)
    if in_house_reservations:
        profIds = [x['reservationGuest']['id'] for x in in_house_reservations]
    else:
        return {'Falha': 'get_in_house_reservation'}

    # Obtem o json completo com todos os cadastros
    profiles_data = get_profiles_by_ids(ids=profIds,hotel=hotel,token=token)
    if profiles_data:
        for x in profiles_data:
            break
    else:
        return {'falha': 'get_profiles_data'}

    # Para cada Reserva
    final_data = []
    for reservation in in_house_reservations:
        
        PROFILE_ID = reservation['reservationGuest']['id']
        profile = [x for x in profiles_data if x['profileIdList'][0]['id'] == PROFILE_ID][0]

        final_data.append({'profId': PROFILE_ID, 'conteudoIteravel': profile})
    
    return {'data': final_data}