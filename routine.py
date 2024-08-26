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
        
        # ----------------------- Reservation Attributes
        RESV_ID = reservation['reservationIdList'][0]['id']
        RESV_CONF = reservation['reservationIdList'][1]['id']
        PROFILE_ID = reservation.get('reservationGuest',{}).get('id','') # Ok
        ARRIVAL_DATE = reservation.get('roomStay', {}).get('arrivalDate','') # Ok
        DEPARTURE_DATE = reservation.get('roomStay',{}).get('departureDate','') # Ok
        ADULT_COUNT = reservation.get('roomStay',{}).get('adultCount','') # Ok
        CHILD_COUNT = reservation.get('roomStay',{}).get('childCount','') # Ok
        ROOM_CLASS = reservation.get('roomStay',{}).get('roomClass','')  # Ok
        ROOM_TYPE = reservation.get('roomStay',{}).get('roomType','') # Ok
        NUMBER_OF_ROOMS = reservation.get('roomStay',{}).get('numberOfRooms','') # Ok
        ROOM_NUMBER = reservation.get('roomStay',{}).get('roomId','') # Ok
        RATE_CODE = reservation.get('roomStay',{}).get('ratePlanCode','') # ok
        RATE_AMOUNT = reservation.get('roomStay',{}).get('rateAmount',{}).get('amount','') # ok
        CURRENCY_CODE = reservation.get('roomStay',{}).get('rateAmount',{}).get('currencyCode','') # ok
        BOOKING_CHANEL_CODE = reservation.get('roomStay',{}).get('bookingChannelCode','') # ok
        FIXED_RATE = reservation.get('roomStay',{}).get('fixedRate','') # ok
        GUARANTEE_CODE = reservation.get('roomStay',{}).get('guarantee',{}).get('guaranteeCode','') # ok
        MARKET_CODE = reservation.get('roomStay',{}).get('marketCode','') # ok
        SOURCE_CODE = reservation.get('roomStay',{}).get('sourceCode','') # ok
        SOURCE_CODE_DESCRIPTION = reservation.get('roomStay',{}).get('sourceCodeDescription','') # ok
        BALANCE_AMOUNT = reservation.get('roomStay',{}).get('balance',{}).get('amount','') # ok
        ROOM_NUMBER_LOCKED = reservation.get('roomStay',{}).get('roomNumberLocked','') # ok
        PSEUDO_ROOM = reservation.get('roomStay',{}).get('pseudoRoom','') # ok
        HAS_SHARE = len(reservation.get('sharedGuests')) > 0
        GUEST_PROFILE_TYPE = reservation.get('reservationGuest',{}).get('nameType','') # ok
        ROOM_STATUS = reservation.get('roomStatus','') # ok
        PAYMENT_METHOD = reservation.get('reservationPaymentMethod',{}).get('paymentMethod','') # ok
        SOURCE_OF_SALE = reservation.get('sourceOfSale',{}).get('sourceType','') # ok
        SOURCE_OF_SALE_CODE = reservation.get('sourceOfSale',{}).get('sourceCode','') # ok
        HOTEL_ID = reservation.get('hotelId','') # ok
        HOTEL_NAME = reservation.get('hotelName','') # ok
        CREATE_DATE_TIME = reservation.get('createDateTime','') # ok
        LAST_MODIFIED_DATE_TIME = reservation.get('lastModifyDateTime','') # ok
        RESERVATION_STATUS = reservation.get('reservationStatus','') # ok
        GUEST_FIRST_NAME = reservation.get('reservationGuest',{}).get('givenName','') # ok
        GUEST_SURNAME = reservation.get('reservationGuest',{}).get('surname','') # ok
        GUEST_LANGUAGE = reservation.get('reservationGuest',{}).get('language','') # ok

        # Get the Json for the profile
        profile = [x for x in profiles_data if x['profileIdList'][0]['id'] == PROFILE_ID][0]


        # ----------------------- Profile Attributes
        TAX_ID = profile.get('profile',{}).get('taxInfo',{}).get('tax1No','') # ok
        GUEST_BIRTH_DATE = profile.get('profile',{}).get('customer',{}).get('birthDate','') # ok
        GENDER = profile.get('profile',{}).get('customer',{}).get('gender', '') # ok

        if not GUEST_BIRTH_DATE:
            GUEST_BIRTH_DATE = ''

        identifications = profile.get('profile',{}).get('customer',{}).get('identifications',False) # ok

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