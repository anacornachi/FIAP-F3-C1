import uuid
from sqlalchemy import Column, String, Float, Boolean, DateTime, ForeignKey, Integer, Date
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from datetime import datetime, timezone


Base = declarative_base()

# Tabela que representa o cadastro de sensores e atuadores físicos
class Component(Base):
    __tablename__ = "components"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    name = Column(String(50), nullable=False)  # Nome do componente
    type = Column(String(30), nullable=False)  # 'Sensor' ou 'Actuator'

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "type": self.type,
        }


# Tabela que armazena os registros de sensores no solo
class SensorRecord(Base):
    __tablename__ = "sensor_records"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    timestamp = Column(DateTime, nullable=False, default=lambda: datetime.now(timezone.utc))  # Momento da coleta
    soil_moisture = Column(Float, nullable=False)  # Umidade do solo (%)
    phosphorus_present = Column(Boolean, nullable=False)  # Presença de fósforo
    potassium_present = Column(Boolean, nullable=False)  # Presença de potássio
    soil_ph = Column(Float, nullable=False)  # Valor de pH do solo
    irrigation_status = Column(String(10), nullable=False)  # Status da irrigação (ATIVADA / DESLIGADA)

    def to_dict(self):
        return {
            "id": self.id,
            "timestamp": self.timestamp.isoformat(),
            "soil_moisture": self.soil_moisture,
            "phosphorus_present": self.phosphorus_present,
            "potassium_present": self.potassium_present,
            "soil_ph": self.soil_ph,
            "irrigation_status": self.irrigation_status,
        }


# Tabela que armazena os dados meteorológicos obtidos de API externa
class ClimateData(Base):
    __tablename__ = "climate_data"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    timestamp = Column(DateTime, nullable=False, default=lambda: datetime.now(timezone.utc))  # Momento da coleta dos dados climáticos
    temperature = Column(Float, nullable=False)  # Temperatura ambiente (°C)
    air_humidity = Column(Float, nullable=False)  # Umidade do ar (%)
    rain_forecast = Column(Boolean, nullable=False)  # Previsão de chuva (True/False)

    def to_dict(self):
        
        return {
            "id": self.id,
            "timestamp": self.timestamp.isoformat(),
            "temperature": self.temperature,
            "air_humidity": self.air_humidity,
            "rain_forecast": self.rain_forecast,
        }

class Produtor(Base):
    __tablename__ = 'produtor'

    id_produtor = Column(Integer, primary_key=True, autoincrement=True)
    nome = Column(String(200), nullable=False)
    email = Column(String(200), nullable=False)
    telefone = Column(String(30), nullable=False)

    # Relacionamentos
    culturas = relationship("Cultura", back_populates="produtor")

    def __repr__(self):
        return f"<Produtor(id={self.id_produtor}, nome='{self.nome}')>"

class Cultura(Base):
    __tablename__ = 'cultura'

    id_cultura = Column(Integer, primary_key=True, autoincrement=True)
    nome = Column(String(100), nullable=False)
    tipo = Column(String(50), nullable=False)
    data_inicio = Column(Date, nullable=False)
    data_fim = Column(Date)
    id_produtor = Column(Integer, ForeignKey('produtor.id_produtor'), nullable=False)

    # Relacionamentos
    produtor = relationship("Produtor", back_populates="culturas")
    sensores = relationship("Sensor", back_populates="cultura")
    aplicacoes = relationship("Aplicacao", back_populates="cultura")

    def __repr__(self):
        return f"<Cultura(id={self.id_cultura}, nome='{self.nome}')>"

class Sensor(Base):
    __tablename__ = 'sensor'

    id_sensor = Column(Integer, primary_key=True, autoincrement=True)
    tipo = Column(String(50), nullable=False)
    modelo = Column(String(50), nullable=False)
    localizacao = Column(String(100), nullable=False)
    id_cultura = Column(Integer, ForeignKey('cultura.id_cultura'), nullable=False)

    # Relacionamentos
    cultura = relationship("Cultura", back_populates="sensores")
    leituras = relationship("LeituraSensor", back_populates="sensor")

    def __repr__(self):
        return f"<Sensor(id={self.id_sensor}, tipo='{self.tipo}')>"

class LeituraSensor(Base):
    __tablename__ = 'leitura_sensor'

    id_leitura = Column(Integer, primary_key=True, autoincrement=True)
    id_sensor = Column(Integer, ForeignKey('sensor.id_sensor'), nullable=False)
    data_hora = Column(DateTime, nullable=False, default=datetime.utcnow)
    valor_umidade = Column(Float)
    valor_ph = Column(Float)
    valor_npk_fosforo = Column(Float)
    valor_npk_potassio = Column(Float)

    # Relacionamentos
    sensor = relationship("Sensor", back_populates="leituras")

    def __repr__(self):
        return f"<LeituraSensor(id={self.id_leitura}, sensor={self.id_sensor}, data={self.data_hora})>"

class Aplicacao(Base):
    __tablename__ = 'aplicacao'

    id_aplicacao = Column(Integer, primary_key=True, autoincrement=True)
    id_cultura = Column(Integer, ForeignKey('cultura.id_cultura'), nullable=False)
    data_hora = Column(DateTime, nullable=False, default=datetime.utcnow)
    tipo = Column(String(50), nullable=False)
    quantidade = Column(Float, nullable=False)

    # Relacionamentos
    cultura = relationship("Cultura", back_populates="aplicacoes")

    def __repr__(self):
        return f"<Aplicacao(id={self.id_aplicacao}, cultura={self.id_cultura}, tipo='{self.tipo}')>"
