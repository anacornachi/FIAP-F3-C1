"""
Serviço para processamento de dados dos sensores.
"""

import logging
from typing import List, Optional, Dict
from datetime import datetime, timedelta

from ..database.models.sensor_data import SensorData
from ..database.repositories.sensor_repository import SensorRepository
from database import get_session, close_session
from database.repositories import LeituraSensorRepository
from config.settings import SENSOR_CONFIG

logger = logging.getLogger(__name__)

class SensorService:

    def __init__(self):
        self.session = get_session()
        self.sensor_repo = SensorRepository(self.session)
        self.leitura_repo = LeituraSensorRepository(self.session)

    def process_sensor_data(self, sensor_data: SensorData) -> SensorData:
        # Lógica para determinar se a irrigação deve ser ativada
        should_irrigate = (
            sensor_data.soil_moisture < 30.0 or  # Umidade muito baixa
            (sensor_data.ph_level < 5.0 or sensor_data.ph_level > 8.0) or  # pH fora do ideal
            not sensor_data.phosphorus_level or  # Falta de fósforo
            not sensor_data.potassium_level  # Falta de potássio
        )
        
        sensor_data.irrigation_active = should_irrigate
        return self.sensor_repo.create(sensor_data)

    def get_sensor_data(self, id: int) -> Optional[SensorData]:
        return self.sensor_repo.get_by_id(id)

    def get_all_sensor_data(self) -> List[SensorData]:
        return self.sensor_repo.get_all()

    def update_sensor_data(self, sensor_data: SensorData) -> Optional[SensorData]:
        return self.sensor_repo.update(sensor_data)

    def delete_sensor_data(self, id: int) -> bool:
        return self.sensor_repo.delete(id)

    def get_sensor_data_by_date_range(self, start_date: datetime, end_date: datetime) -> List[SensorData]:
        return self.sensor_repo.get_by_date_range(start_date, end_date)

    def get_sensor_statistics(self, start_date: datetime, end_date: datetime) -> dict:
        data = self.get_sensor_data_by_date_range(start_date, end_date)
        
        if not data:
            return {
                'average_ph': 0,
                'average_moisture': 0,
                'irrigation_time_percentage': 0,
                'phosphorus_deficiency_percentage': 0,
                'potassium_deficiency_percentage': 0
            }

        total_records = len(data)
        total_irrigation_time = sum(1 for d in data if d.irrigation_active)
        total_phosphorus_deficiency = sum(1 for d in data if not d.phosphorus_level)
        total_potassium_deficiency = sum(1 for d in data if not d.potassium_level)

        return {
            'average_ph': sum(d.ph_level for d in data) / total_records,
            'average_moisture': sum(d.soil_moisture for d in data) / total_records,
            'irrigation_time_percentage': (total_irrigation_time / total_records) * 100,
            'phosphorus_deficiency_percentage': (total_phosphorus_deficiency / total_records) * 100,
            'potassium_deficiency_percentage': (total_potassium_deficiency / total_records) * 100
        }

    def processar_leitura(self, id_sensor: int, dados: Dict[str, float]) -> Optional[Dict]:
        """
        Processa uma leitura de sensor e a armazena no banco de dados.
        
        Args:
            id_sensor: ID do sensor que realizou a leitura
            dados: Dicionário com os valores lidos (umidade, ph, fosforo, potassio)
            
        Returns:
            Dict com os dados processados ou None em caso de erro
        """
        try:
            # Valida o sensor
            sensor = self.sensor_repo.get_by_id(id_sensor)
            if not sensor:
                logger.error(f"Sensor {id_sensor} não encontrado")
                return None

            # Valida os dados
            dados_validados = self._validar_dados(dados)
            if not dados_validados:
                return None

            # Registra a leitura
            leitura = self.leitura_repo.create(
                id_sensor=id_sensor,
                valor_umidade=dados_validados.get('umidade'),
                valor_ph=dados_validados.get('ph'),
                valor_npk_fosforo=dados_validados.get('fosforo'),
                valor_npk_potassio=dados_validados.get('potassio')
            )

            logger.info(f"Leitura registrada com sucesso: {leitura.id_leitura}")
            return self._formatar_leitura(leitura)

        except Exception as e:
            logger.error(f"Erro ao processar leitura: {str(e)}")
            return None
        finally:
            close_session()

    def _validar_dados(self, dados: Dict[str, float]) -> Optional[Dict[str, float]]:
        """
        Valida os dados recebidos dos sensores.
        
        Args:
            dados: Dicionário com os valores lidos
            
        Returns:
            Dict com os dados validados ou None se inválidos
        """
        try:
            dados_validados = {}
            
            # Valida umidade
            if 'umidade' in dados:
                umidade = float(dados['umidade'])
                if SENSOR_CONFIG['umidade']['min'] <= umidade <= SENSOR_CONFIG['umidade']['max']:
                    dados_validados['umidade'] = umidade
                else:
                    logger.warning(f"Umidade fora do intervalo válido: {umidade}")

            # Valida pH
            if 'ph' in dados:
                ph = float(dados['ph'])
                if SENSOR_CONFIG['ph']['min'] <= ph <= SENSOR_CONFIG['ph']['max']:
                    dados_validados['ph'] = ph
                else:
                    logger.warning(f"pH fora do intervalo válido: {ph}")

            # Valida NPK
            if 'fosforo' in dados:
                fosforo = float(dados['fosforo'])
                if SENSOR_CONFIG['npk']['min'] <= fosforo <= SENSOR_CONFIG['npk']['max']:
                    dados_validados['fosforo'] = fosforo
                else:
                    logger.warning(f"Fósforo fora do intervalo válido: {fosforo}")

            if 'potassio' in dados:
                potassio = float(dados['potassio'])
                if SENSOR_CONFIG['npk']['min'] <= potassio <= SENSOR_CONFIG['npk']['max']:
                    dados_validados['potassio'] = potassio
                else:
                    logger.warning(f"Potássio fora do intervalo válido: {potassio}")

            return dados_validados

        except (ValueError, TypeError) as e:
            logger.error(f"Erro ao validar dados: {str(e)}")
            return None

    def _formatar_leitura(self, leitura) -> Dict:
        """
        Formata os dados da leitura para retorno.
        
        Args:
            leitura: Objeto LeituraSensor
            
        Returns:
            Dict com os dados formatados
        """
        return {
            'id': leitura.id_leitura,
            'sensor': leitura.id_sensor,
            'data_hora': leitura.data_hora.isoformat(),
            'umidade': leitura.valor_umidade,
            'ph': leitura.valor_ph,
            'fosforo': leitura.valor_npk_fosforo,
            'potassio': leitura.valor_npk_potassio
        }
