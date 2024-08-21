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

def get_data(hotel, token):

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
        
        #Reserva os valores dos campos de reservas
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
        
        try: RATE_CODE = reservation['roomStay']['ratePlanCode']
        except: RATE_CODE = ''

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

        profile = [x for x in profiles_data if x['profileIdList'][0]['id'] == PROFILE_ID][0]

        TAX_ID = profile.get('profile',{}).get('taxInfo',{}).get('tax1No','')
        GUEST_BIRTH_DATE = profile.get('profile',{}).get('customer',{}).get('birthDate','')
        GENDER = profile.get('profile',{}).get('customer',{}).get('gender', '')

        if not GUEST_BIRTH_DATE:
            GUEST_BIRTH_DATE = ''

        identifications = profile.get('profile',{}).get('customer',{}).get('identifications',False)

        if not identifications:
            CPF = ''
            PASSPORT = ''
            RG = ''
            identifications = []
        else:
            identifications = identifications.get('identificationInfo',[])

        if len(identifications) > 0:
            if len([x for x in identifications if x['identification']['idType'] == 'PAS']) > 0:
                PASSPORT = [x for x in identifications if x['identification']['idType'] == 'PAS'][0]

        for regra in [x for x in regras if x['rule_type'] == 'R']:

            if eval(regra['rule_code']):
                final_data.append({'regra': regra['rule_description'], 'reserva': reservation})
    
    return {'data': final_data}