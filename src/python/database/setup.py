from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from datetime import datetime, date
import os
from dotenv import load_dotenv

from .models import Base, Produtor, Cultura, Sensor, LeituraSensor, Aplicacao

# Carrega variáveis de ambiente
load_dotenv()

# Configuração da conexão com o banco
ORACLE_USER = os.getenv('ORACLE_USER', 'system')
ORACLE_PASSWORD = os.getenv('ORACLE_PASSWORD', 'oracle')
ORACLE_HOST = os.getenv('ORACLE_HOST', 'localhost')
ORACLE_PORT = os.getenv('ORACLE_PORT', '1521')
ORACLE_SERVICE = os.getenv('ORACLE_SERVICE', 'XE')

# String de conexão
DATABASE_URL = f"oracle://{ORACLE_USER}:{ORACLE_PASSWORD}@{ORACLE_HOST}:{ORACLE_PORT}/{ORACLE_SERVICE}"

def init_db():
    """Inicializa o banco de dados criando todas as tabelas."""
    engine = create_engine(DATABASE_URL)
    Base.metadata.create_all(engine)
    
    # Cria uma sessão para inserir dados de exemplo
    Session = sessionmaker(bind=engine)
    session = Session()
    
    try:
        # Verifica se já existem dados
        if session.query(Produtor).first():
            print("Banco de dados já populado.")
            return
        
        # Cria um produtor de exemplo
        produtor = Produtor(
            nome="João Silva",
            email="joao.silva@email.com",
            telefone="(11) 99999-9999"
        )
        session.add(produtor)
        session.commit()
        
        # Cria uma cultura de exemplo
        cultura = Cultura(
            nome="Milho",
            tipo="grão",
            data_inicio=date(2024, 1, 1),
            id_produtor=produtor.id_produtor
        )
        session.add(cultura)
        session.commit()
        
        # Cria sensores de exemplo
        sensores = [
            Sensor(
                tipo="umidade",
                modelo="DHT22",
                localizacao="Setor A",
                id_cultura=cultura.id_cultura
            ),
            Sensor(
                tipo="ph",
                modelo="pH-2000",
                localizacao="Setor B",
                id_cultura=cultura.id_cultura
            )
        ]
        session.add_all(sensores)
        session.commit()
        
        # Cria leituras de exemplo
        for sensor in sensores:
            leitura = LeituraSensor(
                id_sensor=sensor.id_sensor,
                valor_umidade=65.5 if sensor.tipo == "umidade" else None,
                valor_ph=6.5 if sensor.tipo == "ph" else None,
                valor_npk_fosforo=45.0 if sensor.tipo == "ph" else None,
                valor_npk_potassio=35.0 if sensor.tipo == "ph" else None
            )
            session.add(leitura)
        
        # Cria aplicações de exemplo
        aplicacao = Aplicacao(
            id_cultura=cultura.id_cultura,
            tipo="irrigação",
            quantidade=100.0
        )
        session.add(aplicacao)
        
        session.commit()
        print("Banco de dados populado com sucesso!")
        
    except Exception as e:
        session.rollback()
        print(f"Erro ao popular banco de dados: {str(e)}")
        raise
    finally:
        session.close()

if __name__ == "__main__":
    init_db()
