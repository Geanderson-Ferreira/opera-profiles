from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Hotel, Rule, HotelRule, Base

# URL de conexão com o banco de dados
database_url = 'mysql+pymysql://root:TEechOJTIXHIveUbEpKZBViriBYsFSIT@roundhouse.proxy.rlwy.net:11569/railway'

# Conectar ao banco de dados
engine = create_engine(database_url, echo=True)
Session = sessionmaker(bind=engine)
session = Session()

# Adicionar hotéis
hotels = [
    Hotel(hotel_id='H5633', hotel_name='Ibis Joinville'),
    Hotel(hotel_id='H5519', hotel_name='Ibis Budget Curitiba Centro'),
    Hotel(hotel_id='H6665', hotel_name='Novotel Porto Alegre Aeroporto')
]

session.add_all(hotels)
session.commit()

# Adicionar regras
rules = [
    Rule(rule_description='Reserva é RB1', rule_code="RATE_CODE == 'RB1'", rule_type='R'),
    Rule(rule_description='Market Code é TE', rule_code="MARKET_CODE == 'TE'", rule_type='R')
]

session.add_all(rules)
session.commit()

# Obter IDs de regras
rule_ids = [rule.rule_id for rule in session.query(Rule).all()]

# Associar regras a hotéis
hotel_ids = ['H5633', 'H5519', 'H6665']
hotel_rules = [HotelRule(hotel_id=hotel_id, rule_id=rule_id) 
               for hotel_id in hotel_ids 
               for rule_id in rule_ids]

session.add_all(hotel_rules)
session.commit()

# Fechar a sessão
session.close()
