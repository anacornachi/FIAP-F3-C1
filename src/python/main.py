"""
Ponto de entrada principal da aplicação.
"""

import logging
import logging.config
from datetime import datetime
import json
import os
from dotenv import load_dotenv

from config.settings import LOG_CONFIG
from services.sensor_service import SensorService
from services.irrigation_service import IrrigationService

# Configura logging
logging.config.dictConfig(LOG_CONFIG)
logger = logging.getLogger(__name__)

# Carrega variáveis de ambiente
load_dotenv()

def processar_dados_sensor(dados_json: str) -> dict:
    """
    Processa dados recebidos do sensor.
    
    Args:
        dados_json: String JSON com os dados do sensor
        
    Returns:
        Dict com o resultado do processamento
    """
    try:
        # Converte JSON para dict
        dados = json.loads(dados_json)
        
        # Valida dados obrigatórios
        if 'id_sensor' not in dados:
            raise ValueError("ID do sensor não fornecido")
            
        # Processa leitura
        sensor_service = SensorService()
        resultado = sensor_service.processar_leitura(
            id_sensor=dados['id_sensor'],
            dados=dados
        )
        
        if resultado:
            # Verifica necessidade de irrigação
            irrigation_service = IrrigationService()
            status_irrigacao = irrigation_service.verificar_irrigacao(dados['id_sensor'])
            
            return {
                'status': 'sucesso',
                'leitura': resultado,
                'irrigacao': status_irrigacao
            }
        else:
            return {
                'status': 'erro',
                'mensagem': 'Falha ao processar leitura'
            }
            
    except json.JSONDecodeError:
        logger.error("Erro ao decodificar JSON")
        return {
            'status': 'erro',
            'mensagem': 'JSON inválido'
        }
    except Exception as e:
        logger.error(f"Erro ao processar dados: {str(e)}")
        return {
            'status': 'erro',
            'mensagem': str(e)
        }

def main():
    """
    Função principal da aplicação.
    """
    logger.info("Iniciando aplicação...")
    
    # Exemplo de uso
    dados_exemplo = {
        'id_sensor': 1,
        'umidade': 25.5,
        'ph': 6.8,
        'fosforo': 15.0,
        'potassio': 20.0
    }
    
    resultado = processar_dados_sensor(json.dumps(dados_exemplo))
    print(json.dumps(resultado, indent=2))

if __name__ == "__main__":
    main()
