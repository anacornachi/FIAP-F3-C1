import pytest
from datetime import datetime
from typing import Generator

from config.database_config import DatabaseConfig
from database.repositories.sensor_repository import SensorRepository
from services.sensor_service import SensorService
from database.models.sensor_data import SensorData

@pytest.fixture
def db_config() -> DatabaseConfig:
    """Fixture para configuração do banco de dados de teste."""
    return DatabaseConfig(
        host="localhost",
        port=1521,
        database="XE",
        user="system",
        password="oracle"
    )

@pytest.fixture
def sensor_repository(db_config: DatabaseConfig) -> Generator[SensorRepository, None, None]:
    """Fixture para o repositório de sensores."""
    repository = SensorRepository(db_config)
    yield repository
    # Limpa os dados após os testes
    with repository._get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute("DROP TABLE IF EXISTS sensor_data")
            conn.commit()

@pytest.fixture
def sensor_service(sensor_repository: SensorRepository) -> SensorService:
    """Fixture para o serviço de sensores."""
    return SensorService(sensor_repository)

@pytest.fixture
def sample_sensor_data() -> SensorData:
    """Fixture para dados de sensor de exemplo."""
    return SensorData(
        timestamp=datetime.now(),
        phosphorus_level=True,
        potassium_level=True,
        ph_level=6.5,
        soil_moisture=45.0,
        irrigation_active=False
    ) 