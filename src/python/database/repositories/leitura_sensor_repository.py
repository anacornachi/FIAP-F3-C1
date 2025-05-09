from typing import List, Optional
from datetime import datetime
from sqlalchemy.orm import Session
from ..models import LeituraSensor

class LeituraSensorRepository:
    def __init__(self, session: Session):
        self.session = session

    def create(self, id_sensor: int, valor_umidade: float = None, valor_ph: float = None,
               valor_npk_fosforo: float = None, valor_npk_potassio: float = None) -> LeituraSensor:
        leitura = LeituraSensor(
            id_sensor=id_sensor,
            data_hora=datetime.utcnow(),
            valor_umidade=valor_umidade,
            valor_ph=valor_ph,
            valor_npk_fosforo=valor_npk_fosforo,
            valor_npk_potassio=valor_npk_potassio
        )
        self.session.add(leitura)
        self.session.commit()
        return leitura

    def get_by_id(self, id_leitura: int) -> Optional[LeituraSensor]:
        return self.session.query(LeituraSensor).filter(LeituraSensor.id_leitura == id_leitura).first()

    def get_all(self) -> List[LeituraSensor]:
        return self.session.query(LeituraSensor).all()

    def get_by_sensor(self, id_sensor: int) -> List[LeituraSensor]:
        return self.session.query(LeituraSensor).filter(LeituraSensor.id_sensor == id_sensor).all()

    def get_by_date_range(self, start_date: datetime, end_date: datetime) -> List[LeituraSensor]:
        return self.session.query(LeituraSensor).filter(
            LeituraSensor.data_hora.between(start_date, end_date)
        ).all()

    def get_latest_by_sensor(self, id_sensor: int) -> Optional[LeituraSensor]:
        return self.session.query(LeituraSensor).filter(
            LeituraSensor.id_sensor == id_sensor
        ).order_by(LeituraSensor.data_hora.desc()).first()

    def delete(self, id_leitura: int) -> bool:
        leitura = self.get_by_id(id_leitura)
        if leitura:
            self.session.delete(leitura)
            self.session.commit()
            return True
        return False

    def get_average_values_by_sensor(self, id_sensor: int, start_date: datetime = None, 
                                   end_date: datetime = None) -> dict:
        query = self.session.query(LeituraSensor).filter(LeituraSensor.id_sensor == id_sensor)
        
        if start_date and end_date:
            query = query.filter(LeituraSensor.data_hora.between(start_date, end_date))
        
        leituras = query.all()
        
        if not leituras:
            return {
                'umidade': 0,
                'ph': 0,
                'fosforo': 0,
                'potassio': 0
            }
        
        return {
            'umidade': sum(l.valor_umidade or 0 for l in leituras) / len(leituras),
            'ph': sum(l.valor_ph or 0 for l in leituras) / len(leituras),
            'fosforo': sum(l.valor_npk_fosforo or 0 for l in leituras) / len(leituras),
            'potassio': sum(l.valor_npk_potassio or 0 for l in leituras) / len(leituras)
        } 