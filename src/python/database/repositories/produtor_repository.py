from typing import List, Optional
from sqlalchemy.orm import Session
from ..models import Produtor

class ProdutorRepository:
    def __init__(self, session: Session):
        self.session = session

    def create(self, nome: str, email: str, telefone: str) -> Produtor:
        produtor = Produtor(
            nome=nome,
            email=email,
            telefone=telefone
        )
        self.session.add(produtor)
        self.session.commit()
        return produtor

    def get_by_id(self, id_produtor: int) -> Optional[Produtor]:
        return self.session.query(Produtor).filter(Produtor.id_produtor == id_produtor).first()

    def get_all(self) -> List[Produtor]:
        return self.session.query(Produtor).all()

    def update(self, id_produtor: int, nome: str = None, email: str = None, telefone: str = None) -> Optional[Produtor]:
        produtor = self.get_by_id(id_produtor)
        if produtor:
            if nome is not None:
                produtor.nome = nome
            if email is not None:
                produtor.email = email
            if telefone is not None:
                produtor.telefone = telefone
            self.session.commit()
        return produtor

    def delete(self, id_produtor: int) -> bool:
        produtor = self.get_by_id(id_produtor)
        if produtor:
            self.session.delete(produtor)
            self.session.commit()
            return True
        return False

    def get_by_email(self, email: str) -> Optional[Produtor]:
        return self.session.query(Produtor).filter(Produtor.email == email).first() 