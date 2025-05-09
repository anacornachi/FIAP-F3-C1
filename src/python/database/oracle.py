from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
import os
from dotenv import load_dotenv

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

# Cria o engine do SQLAlchemy
engine = create_engine(DATABASE_URL)

# Cria a sessão
session_factory = sessionmaker(bind=engine)
Session = scoped_session(session_factory)

def get_session():
    """Retorna uma nova sessão do banco de dados."""
    return Session()

def close_session():
    """Fecha a sessão atual."""
    Session.remove()

class DB:
    session = Session
    engine = engine

db = DB()
