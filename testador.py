from src.models_methods import create_rule
from src.models_methods import create_rule, assign_rule_to_hotel
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from src.models import *

engine = create_engine(environ['DB_CONNECTION'], echo=False)
Session = sessionmaker(bind=engine)

descricao_da_regra = "CPF está vazio"
codigo_da_regra = "TAX_ID == ''"
categoria = "R"

# create_rule(Session(), descricao_da_regra,codigo_da_regra,categoria, True)

# engine = create_engine(environ['DB_CONNECTION'], echo=False)
# Session = sessionmaker(bind=engine)

# assign_rule_to_hotel(Session(), 'H5519', 3)