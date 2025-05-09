"""
Serviço para controle de irrigação baseado nas leituras dos sensores.
"""

import logging
from datetime import datetime
from typing import Dict, Optional

from database import get_session, close_session
from database.repositories import LeituraSensorRepository, AplicacaoRepository
from config.settings import IRRIGATION_CONFIG

logger = logging.getLogger(__name__)

class IrrigationService:
    def __init__(self):
        self.session = get_session()
        self.leitura_repo = LeituraSensorRepository(self.session)
        self.aplicacao_repo = AplicacaoRepository(self.session)

    def verificar_irrigacao(self, id_sensor: int) -> Dict:
        try:
            # Obtém a última leitura do sensor
            ultima_leitura = self.leitura_repo.get_latest_by_sensor(id_sensor)
            if not ultima_leitura:
                logger.warning(f"Nenhuma leitura encontrada para o sensor {id_sensor}")
                return {
                    'irrigar': False,
                    'motivo': 'Sem leituras disponíveis'
                }

            # Verifica a umidade
            if ultima_leitura.valor_umidade is None:
                logger.warning(f"Leitura sem valor de umidade para o sensor {id_sensor}")
                return {
                    'irrigar': False,
                    'motivo': 'Leitura sem valor de umidade'
                }

            # Verifica se precisa irrigar
            precisa_irrigar = ultima_leitura.valor_umidade < IRRIGATION_CONFIG['umidade_minima']
            
            if precisa_irrigar:
                # Registra a aplicação de irrigação
                self.aplicacao_repo.create(
                    id_cultura=ultima_leitura.sensor.id_cultura,
                    tipo='irrigação',
                    quantidade=IRRIGATION_CONFIG['duracao_irrigacao']
                )
                logger.info(f"Irrigação iniciada para o sensor {id_sensor}")
                return {
                    'irrigar': True,
                    'motivo': f'Umidade baixa: {ultima_leitura.valor_umidade}%'
                }
            else:
                return {
                    'irrigar': False,
                    'motivo': f'Umidade adequada: {ultima_leitura.valor_umidade}%'
                }

        except Exception as e:
            logger.error(f"Erro ao verificar irrigação: {str(e)}")
            return {
                'irrigar': False,
                'motivo': f'Erro: {str(e)}'
            }
        finally:
            close_session()

    def obter_estatisticas_irrigacao(self, id_cultura: int, 
                                   data_inicio: datetime = None,
                                   data_fim: datetime = None) -> Dict:
        try:
            # Obtém todas as aplicações de irrigação
            aplicacoes = self.aplicacao_repo.get_by_cultura(id_cultura)
            if data_inicio and data_fim:
                aplicacoes = [a for a in aplicacoes 
                            if data_inicio <= a.data_hora <= data_fim]

            # Calcula estatísticas
            total_aplicacoes = len(aplicacoes)
            duracao_total = sum(a.quantidade for a in aplicacoes)
            
            return {
                'total_aplicacoes': total_aplicacoes,
                'duracao_total': duracao_total,
                'duracao_media': duracao_total / total_aplicacoes if total_aplicacoes > 0 else 0,
                'primeira_aplicacao': aplicacoes[0].data_hora if aplicacoes else None,
                'ultima_aplicacao': aplicacoes[-1].data_hora if aplicacoes else None
            }

        except Exception as e:
            logger.error(f"Erro ao obter estatísticas: {str(e)}")
            return {
                'erro': str(e)
            }
        finally:
            close_session() 