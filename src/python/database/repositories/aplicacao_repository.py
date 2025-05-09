from typing import List, Optional
from datetime import datetime
from sqlalchemy.orm import Session
from ..models import Aplicacao

class AplicacaoRepository:
    def __init__(self, session: Session):
        self.session = session

    def create(self, id_cultura: int, tipo: str, quantidade: float) -> Aplicacao:
        aplicacao = Aplicacao(
            id_cultura=id_cultura,
            data_hora=datetime.utcnow(),
            tipo=tipo,
            quantidade=quantidade
        )
        self.session.add(aplicacao)
        self.session.commit()
        return aplicacao

    def get_by_id(self, id_aplicacao: int) -> Optional[Aplicacao]:
        return self.session.query(Aplicacao).filter(Aplicacao.id_aplicacao == id_aplicacao).first()

    def get_all(self) -> List[Aplicacao]:
        return self.session.query(Aplicacao).all()

    def get_by_cultura(self, id_cultura: int) -> List[Aplicacao]:
        return self.session.query(Aplicacao).filter(Aplicacao.id_cultura == id_cultura).all()

    def get_by_date_range(self, start_date: datetime, end_date: datetime) -> List[Aplicacao]:
        return self.session.query(Aplicacao).filter(
            Aplicacao.data_hora.between(start_date, end_date)
        ).all()

    def get_by_type(self, tipo: str) -> List[Aplicacao]:
        return self.session.query(Aplicacao).filter(Aplicacao.tipo == tipo).all()

    def delete(self, id_aplicacao: int) -> bool:
        aplicacao = self.get_by_id(id_aplicacao)
        if aplicacao:
            self.session.delete(aplicacao)
            self.session.commit()
            return True
        return False

    def get_total_quantity_by_type(self, tipo: str, start_date: datetime = None, 
                                 end_date: datetime = None) -> float:
        query = self.session.query(Aplicacao).filter(Aplicacao.tipo == tipo)
        
        if start_date and end_date:
            query = query.filter(Aplicacao.data_hora.between(start_date, end_date))
        
        aplicacoes = query.all()
        return sum(a.quantidade for a in aplicacoes)

    def get_culture_application_summary(self, id_cultura: int) -> dict:
        aplicacoes = self.get_by_cultura(id_cultura)
        
        if not aplicacoes:
            return {
                'total_aplicacoes': 0,
                'tipos_aplicados': [],
                'quantidade_total': 0
            }
        
        tipos = set(a.tipo for a in aplicacoes)
        quantidade_total = sum(a.quantidade for a in aplicacoes)
        
        return {
            'total_aplicacoes': len(aplicacoes),
            'tipos_aplicados': list(tipos),
            'quantidade_total': quantidade_total
        } 