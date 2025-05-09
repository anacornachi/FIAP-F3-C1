from datetime import datetime
from dataclasses import dataclass
from typing import Optional

@dataclass
class SensorData:
    """Modelo para os dados dos sensores."""
    id: Optional[int] = None
    timestamp: datetime = datetime.now()
    phosphorus_level: bool = False  # True = presente, False = ausente
    potassium_level: bool = False   # True = presente, False = ausente
    ph_level: float = 0.0          # Valor entre 0 e 14
    soil_moisture: float = 0.0     # Valor da umidade do solo
    irrigation_active: bool = False # Status da irrigação

    def to_dict(self) -> dict:
        """Converte o objeto para um dicionário."""
        return {
            'id': self.id,
            'timestamp': self.timestamp.isoformat(),
            'phosphorus_level': self.phosphorus_level,
            'potassium_level': self.potassium_level,
            'ph_level': self.ph_level,
            'soil_moisture': self.soil_moisture,
            'irrigation_active': self.irrigation_active
        }

    @classmethod
    def from_dict(cls, data: dict) -> 'SensorData':
        """Cria um objeto SensorData a partir de um dicionário."""
        return cls(
            id=data.get('id'),
            timestamp=datetime.fromisoformat(data['timestamp']) if isinstance(data.get('timestamp'), str) else data.get('timestamp'),
            phosphorus_level=data.get('phosphorus_level', False),
            potassium_level=data.get('potassium_level', False),
            ph_level=data.get('ph_level', 0.0),
            soil_moisture=data.get('soil_moisture', 0.0),
            irrigation_active=data.get('irrigation_active', False)
        ) 