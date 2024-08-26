from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Hotel, Rule, HotelRule, Base
from os import environ
from dotenv import load_dotenv

load_dotenv()

# URL de conexão com o banco de dados
database_url = environ['DB_CONNECTION']

# Configuração do motor de banco de dados
engine = create_engine(database_url, echo=False)  # Ajuste o echo para False em produção

# Configuração da sessão
Session = sessionmaker(bind=engine)

# Inserir dados no banco
def insert_data():
    with Session() as session:
        # Inserir hotéis
        hotels_data = [
            ('H0768', "MERCURE JOINVILLE PRINZ"), ('H3624', "MERCURE JARAGUA DO SUL"), 
            ('H3736', "IBIS CURITIBA AEROPORTO"), ('H5021', "IBIS GUARULHOS"), 
            ('H5168', "MERCURE SAO JOSE DOS CAMPOS"), ('H5181', "MERCURE CAMPINAS"), 
            ('H5468', "IBIS BLUMENAU"), ('H5469', "IBIS CAMPINAS"), ('H5470', "IBIS CAXIAS DO SUL"), 
            ('H5519', "IBIS BUDGET CURITIBA"), ('H5521', "IBIS BUDGET RIO DE JANEIRO CENTRO"), 
            ('H5528', "IBIS VITORIA AEROPORTO"), ('H5534', "IBIS RIO DE JANEIRO CENTRO"), 
            ('H5541', "IBIS ARACATUBA"), ('H5633', "IBIS JOINVILLE"), ('H5670', "IBIS POA AEROPORTO"), 
            ('H5672', "IBIS SANTO ANDRE"), ('H6035', "IBIS SAO JOSE DOS CAMPOS COLINAS"), 
            ('H6315', "IBIS CRICIUMA"), ('H6664', "IBIS POA MOINHOS"), ('H6665', "NOVOTEL POA AEROPORTO"), 
            ('H6969', "IBIS POCOS DE CALDAS"), ('H7220', "IBIS BUDGET VITORIA"), 
            ('H7823', "IBIS MOGI DAS CRUZES"), ('H8175', "IBIS NOVO HAMBURGO"), 
            ('H8273', "IBIS CANOAS"), ('H8279', "IBIS ITATIBA"), ('H8637', "IBIS JACAREI"), 
            ('H8638', "IBIS GUARATINGUETA"), ('H8649', "NOVOTEL SANTOS GONZAGA"), 
            ('H8664', "IBIS LONDRINA"), ('H8665', "IBIS GUAIBA"), ('H9038', "IBIS SANTOS VALONGO"), 
            ('H9087', "IBIS POA ASSIS BRASIL"), ('H9088', "NOVOTEL CURITIBA BATEL"), 
            ('H9089', "IBIS STYLES POA CENTRO"), ('H9190', "IBIS JUNDIAI"), 
            ('H9360', "IBIS CARLOS BARBOSA"), ('H9362', "IBIS CHAPECO"), 
            ('H9382', "IBIS BUDGET BLUMENAU"), ('H9564', "MERCURE ITAJAI NAVEGANTES"), 
            ('H9611', "IBIS BUDGET SANTOS GONZAGA"), ('H9719', "IBIS BUDGET CURITIBA AERO"), 
            ('H9956', "IBIS BUDGET FOZ DO IGUACU"), ('HA0G6', "IBIS IGREJINHA"), 
            ('HA487', "IBIS PONTA GROSSA"), ('HA8F7', "NOVOTEL CRICIUMA"), 
            ('HB1Z6', "IBIS STYLES BELEM BATISTA CAMPOS"), ('HB1Z9', "IBIS STYLES BELEM NAZARE"), 
            ('HB203', "MERCURE BELEM BOULEVARD"), ('HB2Z2', "IBIS STYLES BAURU"), 
            ('HB2Z5', "IBIS STYLES FRANCA"), ('HB2Z6', "IBIS STYLES RIO DE JANEIRO"), 
            ('HB2Z7', "IBIS STYLES RIBEIRAO PRETO BRAZ OLAIA"), ('HB2Z8', "IBIS STYLES PIRACICABA"), 
            ('HB2Z9', "IBIS STYLES RIBEIRAO PRETO MAURILIO BIAGI"), ('HB300', "IBIS STYLES RONDONOPOLIS"), 
            ('HB301', "IBIS STYLES SAO JOSE DO RIO PRETO"), ('HB303', "IBIS STYLES ARARAQUARA"), 
            ('HB304', "IBIS STYLES PARAUAPEBAS"), ('HB305', "IBIS STYLES MARACANAU"), 
            ('HB306', "IBIS STYLES BOA VISTA"), ('HB307', "IBIS STYLES ALAGOINHAS"), 
            ('HB308', "IBIS STYLES POUSO ALEGRE"), ('HB309', "IBIS STYLES PALMAS"), 
            ('HB445', "IBIS BUDGET SAO CAETANO"), ('HB5A2', "IBIS TUBARAO"), 
            ('HB5R1', "IBIS STYLES POCOS DE CALDAS"), ('HB608', "IBIS STYLES CURITIBA AERO"), 
            ('HB609', "IBIS STYLES POA MOINHOS"), ('HB8P5', "GRAND MERCURE RAYON"), 
            ('HB9K6', "IBIS STYLES BELEM HANGAR"), ('HB9K8', "IBIS STYLES BELEM DO PARA"), 
            ('HC0V8', "IBIS STYLES CAMPINAS ALPHAVILLE"), ('HC1D3', "IBIS STYLES MANAUS"), 
            ('HC1X6', "IBIS STYLES GOIANIA SHOPPING ESTACAO")
        ]

        # Inserir hotéis em lotes
        batch_size = 100  # Ajuste conforme necessário
        for i in range(0, len(hotels_data), batch_size):
            batch = hotels_data[i:i+batch_size]
            session.bulk_insert_mappings(Hotel, [{'hotel_id': h_id, 'hotel_name': h_name} for h_id, h_name in batch])
        session.commit()

        # Adicionar regras
        rules = [
            Rule(rule_description='CPF está vazio', rule_code="TAX_ID == '' and not PSEUDO_ROOM", rule_type='R'),
            Rule(rule_description='Data de Nascimento está vazia', rule_code="GUEST_BIRTH_DATE == '' and not PSEUDO_ROOM", rule_type='R'),
            Rule(rule_description='TaxId 9999... e não possui passaporte', rule_code="TAX_ID == '99999999999' and not PSEUDO_ROOM and PASSPORT == ''", rule_type='R'),
            Rule(rule_description='Genero do hospede não informado', rule_code="GENDER == '' and not PSEUDO_ROOM", rule_type='R'),
            Rule(rule_description='TaxId 0000... e não possui passaporte', rule_code="TAX_ID == '00000000000' and not PSEUDO_ROOM and PASSPORT == ''", rule_type='R')
        ]

        session.bulk_save_objects(rules)
        session.commit()

        # Obter IDs de regras e hotéis
        rule_ids = [rule.rule_id for rule in session.query(Rule).all()]
        hotel_ids = [hotel.hotel_id for hotel in session.query(Hotel).all()]

        # Associar regras a todos os hotéis
        hotel_rules = [HotelRule(hotel_id=hotel_id, rule_id=rule_id) 
                       for hotel_id in hotel_ids 
                       for rule_id in rule_ids]
        
        session.bulk_save_objects(hotel_rules)
        session.commit()

# Executar a inserção de dados
if __name__ == '__main__':
    insert_data()
