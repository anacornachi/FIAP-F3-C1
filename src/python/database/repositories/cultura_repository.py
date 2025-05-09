from typing import List, Optional
from datetime import date
from sqlalchemy.orm import Session
from ..models import Cultura

class CulturaRepository:
    def __init__(self, session: Session):
        self.session = session

    def create(self, nome: str, tipo: str, data_inicio: date, id_produtor: int, data_fim: date = None) -> Cultura:
        cultura = Cultura(
            nome=nome,
            tipo=tipo,
            data_inicio=data_inicio,
            data_fim=data_fim,
            id_produtor=id_produtor
        )
        self.session.add(cultura)
        self.session.commit()
        return cultura

    def get_by_id(self, id_cultura: int) -> Optional[Cultura]:
        return self.session.query(Cultura).filter(Cultura.id_cultura == id_cultura).first()

    def get_all(self) -> List[Cultura]:
        return self.session.query(Cultura).all()

    def get_by_produtor(self, id_produtor: int) -> List[Cultura]:
        return self.session.query(Cultura).filter(Cultura.id_produtor == id_produtor).all()

    def update(self, id_cultura: int, nome: str = None, tipo: str = None, 
               data_inicio: date = None, data_fim: date = None) -> Optional[Cultura]:
        cultura = self.get_by_id(id_cultura)
        if cultura:
            if nome is not None:
                cultura.nome = nome
            if tipo is not None:
                cultura.tipo = tipo
            if data_inicio is not None:
                cultura.data_inicio = data_inicio
            if data_fim is not None:
                cultura.data_fim = data_fim
            self.session.commit()
        return cultura

    def delete(self, id_cultura: int) -> bool:
        cultura = self.get_by_id(id_cultura)
        if cultura:
            self.session.delete(cultura)
            self.session.commit()
            return True
        return False

    def get_active_cultures(self) -> List[Cultura]:
        return self.session.query(Cultura).filter(Cultura.data_fim.is_(None)).all()

    def get_cultures_by_type(self, tipo: str) -> List[Cultura]:
        return self.session.query(Cultura).filter(Cultura.tipo == tipo).all() 