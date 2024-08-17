from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from src.models import *

def insert_hotel(session, hotel_id, hotel_name):
    new_hotel = Hotel(hotel_id=hotel_id, hotel_name=hotel_name)
    session.add(new_hotel)
    session.commit()
    print(f"Hotel '{hotel_name}' inserted with ID '{hotel_id}'.")

def create_rule(session, rule_description, rule_code, rule_type, is_active):
    new_rule = Rule(
        rule_description=rule_description,
        rule_code=rule_code,
        rule_type=rule_type,
        is_active=is_active
    )
    session.add(new_rule)
    session.commit()
    print(f"Rule '{rule_description}' created with ID {new_rule.rule_id}.")

def assign_rule_to_hotel(session, hotel_id, rule_id):
    hotel_rule = HotelRule(hotel_id=hotel_id, rule_id=rule_id)
    session.add(hotel_rule)
    session.commit()
    print(f"Rule with ID {rule_id} assigned to hotel with ID '{hotel_id}'.")

def delete_rule(session, rule_id):
    rule_to_delete = session.query(Rule).filter_by(rule_id=rule_id).first()
    if rule_to_delete:
        session.delete(rule_to_delete)
        session.commit()
        print(f"Rule with ID {rule_id} deleted.")
    else:
        print(f"Rule with ID {rule_id} not found.")


def activate_rule(session, rule_id):
    rule_to_activate = session.query(Rule).filter_by(rule_id=rule_id).first()
    if rule_to_activate:
        rule_to_activate.is_active = True
        session.commit()
        print(f"Rule with ID {rule_id} activated.")
    else:
        print(f"Rule with ID {rule_id} not found.")

def deactivate_rule(session, rule_id):
    rule_to_deactivate = session.query(Rule).filter_by(rule_id=rule_id).first()
    if rule_to_deactivate:
        rule_to_deactivate.is_active = False
        session.commit()
        print(f"Rule with ID {rule_id} deactivated.")
    else:
        print(f"Rule with ID {rule_id} not found.")


def get_active_rules_for_hotel(session, hotel_id):
    """
    Retorna todas as regras ativas de um hotel específico.

    :param session: Sessão do banco de dados.
    :param hotel_id: ID do hotel.
    :return: Lista de dicionários contendo informações das regras.
    """
    active_rules = (
        session.query(Rule.rule_description, Rule.rule_code, Rule.rule_type)
        .join(HotelRule, HotelRule.rule_id == Rule.rule_id)
        .filter(HotelRule.hotel_id == hotel_id, Rule.is_active == True)
        .all()
    )
    
    active_rules_list = [
        {
            "rule_description": rule.rule_description,
            "rule_code": rule.rule_code,
            "rule_type": rule.rule_type
        }
        for rule in active_rules
    ]
    
    return active_rules_list