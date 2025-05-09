from typing import List, Optional
from sqlalchemy.orm import Session
from ..models import Sensor

class SensorRepository:
    def __init__(self, session: Session):
        self.session = session

    def create(self, tipo: str, modelo: str, localizacao: str, id_cultura: int) -> Sensor:
        sensor = Sensor(
            tipo=tipo,
            modelo=modelo,
            localizacao=localizacao,
            id_cultura=id_cultura
        )
        self.session.add(sensor)
        self.session.commit()
        return sensor

    def get_by_id(self, id_sensor: int) -> Optional[Sensor]:
        return self.session.query(Sensor).filter(Sensor.id_sensor == id_sensor).first()

    def get_all(self) -> List[Sensor]:
        return self.session.query(Sensor).all()

    def get_by_cultura(self, id_cultura: int) -> List[Sensor]:
        return self.session.query(Sensor).filter(Sensor.id_cultura == id_cultura).all()

    def update(self, id_sensor: int, tipo: str = None, modelo: str = None, 
               localizacao: str = None, id_cultura: int = None) -> Optional[Sensor]:
        sensor = self.get_by_id(id_sensor)
        if sensor:
            if tipo is not None:
                sensor.tipo = tipo
            if modelo is not None:
                sensor.modelo = modelo
            if localizacao is not None:
                sensor.localizacao = localizacao
            if id_cultura is not None:
                sensor.id_cultura = id_cultura
            self.session.commit()
        return sensor

    def delete(self, id_sensor: int) -> bool:
        sensor = self.get_by_id(id_sensor)
        if sensor:
            self.session.delete(sensor)
            self.session.commit()
            return True
        return False

    def get_by_type(self, tipo: str) -> List[Sensor]:
        return self.session.query(Sensor).filter(Sensor.tipo == tipo).all()

    def get_by_model(self, modelo: str) -> List[Sensor]:
        return self.session.query(Sensor).filter(Sensor.modelo == modelo).all() 