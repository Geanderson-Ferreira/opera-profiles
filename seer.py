from tqdm import tqdm
from token_manager import Token
from base_hoteis import Hoteis
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


counter = 0
while counter < 1:#True:
    counter += 1

    #Obtem lista de hoteis do Firebase
    # hoteis = Hoteis().hoteis_from_base("HoteisACC2")
    hoteis = ['H5633']

    #Pega o token
    token = Token().get_token()

    # Para cada hotel
    for hotel in tqdm(hoteis, desc=f"[{counter}] Processando Hotéis", leave=True, colour='green'):

        final_data = []

        engine = create_engine(environ['DB_CONNECTION'], echo=False)
        Session = sessionmaker(bind=engine)
        regras = get_active_rules_for_hotel(session=Session(),hotel_id=hotel)

        # Obter a lista de cadastros das reservas inHouse
        try:
            in_house_reservations = get_in_house(hotel, token)
            profIds = [x['reservationGuest']['id'] for x in in_house_reservations]
        except:
            token = Token().get_token()
            in_house_reservations = get_in_house(hotel, token)
            profIds = [x['reservationGuest']['id'] for x in in_house_reservations]

        # Obtem o json completo com todos os cadastros
        try:
            profiles_data = get_profiles_by_ids(ids=profIds,hotel=hotel,token=token)
            for x in profiles_data:
                break
        except:
            token = Token().get_token()
            profiles_data = get_profiles_by_ids(ids=profIds,hotel=hotel,token=token)
            for x in profiles_data:
                break

        # Para cada Reserva
        for reservation in tqdm(in_house_reservations, desc="Processando Perfis", leave=False):
            
            RESV_ID = reservation['reservationIdList'][0]['id']
            RESV_CONF = reservation['reservationIdList'][1]['id']
            PROFILE_ID = reservation['reservationGuest']['id']
            ARRIVAL_DATE = reservation['roomStay']['arrivalDate']
            DEPARTURE_DATE = reservation['roomStay']['departureDate']
            ADULT_COUNT = reservation['roomStay']['adultCount']
            CHILD_COUNT = reservation['roomStay']['childCount']
            ROOM_CLASS = reservation['roomStay']['roomClass']
            ROOM_TYPE = reservation['roomStay']['roomType']
            NUMBER_OF_ROOMS = reservation['roomStay']['numberOfRooms']
            ROOM_NUMBER = reservation['roomStay']['roomId']
            RATE_CODE = reservation['roomStay']['ratePlanCode']
            RATE_AMOUNT = reservation['roomStay']['rateAmount']['amount']
            CURRENCY_CODE = reservation['roomStay']['rateAmount']['currencyCode']
            BOOKING_CHANEL_CODE = reservation.get('roomStay',{}).get('bookingChannelCode','')
            FIXED_RATE = reservation['roomStay']['fixedRate']
            GUARANTEE_CODE = reservation['roomStay']['guarantee']['guaranteeCode']
            MARKET_CODE = reservation['roomStay']['marketCode']
            SOURCE_CODE = reservation['roomStay']['sourceCode']
            SOURCE_CODE_DESCRIPTION = reservation['roomStay']['sourceCodeDescription']
            BALANCE_AMOUNT = reservation['roomStay']['balance']['amount']
            ROOM_NUMBER_LOCKED = reservation['roomStay']['roomNumberLocked']
            PSEUDO_ROOM = reservation['roomStay']['pseudoRoom']
            HAS_SHARE = len(reservation.get('sharedGuests')) > 0
            GUEST_PROFILE_TYPE = reservation['reservationGuest']['nameType']
            ROOM_STATUS = reservation['roomStatus']
            PAYMENT_METHOD = reservation['reservationPaymentMethod']['paymentMethod']
            SOURCE_OF_SALE = reservation['sourceOfSale']['sourceType']
            SOURCE_OF_SALE_CODE = reservation['sourceOfSale']['sourceCode']
            HOTEL_ID = reservation['hotelId']
            HOTEL_NAME = reservation['hotelName']
            CREATE_DATE_TIME = reservation['createDateTime']
            LAST_MODIFIED_DATE_TIME = reservation['lastModifyDateTime']
            RESERVATION_STATUS = reservation['reservationStatus']
            GUEST_FIRST_NAME = reservation.get('reservationGuest',{}).get('givenName','')
            GUEST_SURNAME = reservation.get('reservationGuest',{}).get('surname','')
            GUEST_LANGUAGE = reservation.get('reservationGuest',{}).get('language','')

            # profile = [x for x in profiles_data if x['profileIdList'][0]['id'] == PROFILE_ID][0]
            # # print(profile, '\n\n')

            # if len(profile['profileIdList']) > 1:
            #     if profile['profileIdList'][1]['type'] == 'CorporateId':
            #         PROFILE_CORPORATE_ID = profile['profileIdList'][1]['id']
            #     else:
            #         PROFILE_CORPORATE_ID = ''

            # ADDRESSESS_COUNT = len(profile['profile']['addresses']['addressInfo'])

            # if len(ADDRESSESS_COUNT) > 0:
            #     GUEST_ADDRESS = ''

            # lista = [PROFILE_CORPORATE_ID, PROFILE_ID, GUEST_ADDRESS]

            # print("\nRESERVA:", RESV_CONF)
            # for i in lista:
            #     print(i)
            # print(profile)

            for regra in [x for x in regras if x['rule_type'] == 'R']:

                if eval(regra['rule_code']):
                    print(f'Reserva {RESV_CONF} foi pego da regra {regra['rule_description']}')
                    final_data.append({'regra': regra['rule_description'], 'reserva': reservation})
            
