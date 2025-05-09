"""
Configurações gerais do projeto.
"""

import os
from dotenv import load_dotenv

# Carrega variáveis de ambiente
load_dotenv()

# Configurações do Banco de Dados
DB_CONFIG = {
    'user': os.getenv('ORACLE_USER', 'system'),
    'password': os.getenv('ORACLE_PASSWORD', 'oracle'),
    'host': os.getenv('ORACLE_HOST', 'localhost'),
    'port': os.getenv('ORACLE_PORT', '1521'),
    'service': os.getenv('ORACLE_SERVICE', 'XE')
}

# Configurações de Logging
LOG_CONFIG = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'standard': {
            'format': '%(asctime)s [%(levelname)s] %(name)s: %(message)s'
        },
    },
    'handlers': {
        'default': {
            'level': 'INFO',
            'formatter': 'standard',
            'class': 'logging.StreamHandler',
        },
        'file': {
            'level': 'INFO',
            'formatter': 'standard',
            'class': 'logging.FileHandler',
            'filename': 'logs/app.log',
            'mode': 'a',
        },
    },
    'loggers': {
        '': {
            'handlers': ['default', 'file'],
            'level': 'INFO',
            'propagate': True
        }
    }
}

# Configurações dos Sensores
SENSOR_CONFIG = {
    'umidade': {
        'min': 0,
        'max': 100,
        'unidade': '%'
    },
    'ph': {
        'min': 0,
        'max': 14,
        'unidade': 'pH'
    },
    'npk': {
        'min': 0,
        'max': 100,
        'unidade': 'mg/kg'
    }
}

# Configurações de Irrigação
IRRIGATION_CONFIG = {
    'umidade_minima': 30,  # Porcentagem
    'umidade_maxima': 80,  # Porcentagem
    'intervalo_verificacao': 300,  # Segundos
    'duracao_irrigacao': 60  # Segundos
} 