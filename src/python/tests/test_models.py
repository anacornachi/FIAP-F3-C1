import pytest
from datetime import datetime

from ..database.models.sensor_data import SensorData

def test_sensor_data_creation():
    timestamp = datetime.now()
    sensor_data = SensorData(
        id=1,
        timestamp=timestamp,
        phosphorus_level=True,
        potassium_level=False,
        ph_level=6.5,
        soil_moisture=45.0,
        irrigation_active=True
    )

    assert sensor_data.id == 1
    assert sensor_data.timestamp == timestamp
    assert sensor_data.phosphorus_level is True
    assert sensor_data.potassium_level is False
    assert sensor_data.ph_level == 6.5
    assert sensor_data.soil_moisture == 45.0
    assert sensor_data.irrigation_active is True

def test_sensor_data_to_dict():
    timestamp = datetime.now()
    sensor_data = SensorData(
        id=1,
        timestamp=timestamp,
        phosphorus_level=True,
        potassium_level=False,
        ph_level=6.5,
        soil_moisture=45.0,
        irrigation_active=True
    )

    data_dict = sensor_data.to_dict()
    assert data_dict['id'] == 1
    assert data_dict['timestamp'] == timestamp.isoformat()
    assert data_dict['phosphorus_level'] is True
    assert data_dict['potassium_level'] is False
    assert data_dict['ph_level'] == 6.5
    assert data_dict['soil_moisture'] == 45.0
    assert data_dict['irrigation_active'] is True

def test_sensor_data_from_dict():
    timestamp = datetime.now()
    data_dict = {
        'id': 1,
        'timestamp': timestamp.isoformat(),
        'phosphorus_level': True,
        'potassium_level': False,
        'ph_level': 6.5,
        'soil_moisture': 45.0,
        'irrigation_active': True
    }

    sensor_data = SensorData.from_dict(data_dict)
    assert sensor_data.id == 1
    assert isinstance(sensor_data.timestamp, datetime)
    assert sensor_data.phosphorus_level is True
    assert sensor_data.potassium_level is False
    assert sensor_data.ph_level == 6.5
    assert sensor_data.soil_moisture == 45.0
    assert sensor_data.irrigation_active is True

def test_sensor_data_default_values():
    sensor_data = SensorData()
    assert sensor_data.id is None
    assert isinstance(sensor_data.timestamp, datetime)
    assert sensor_data.phosphorus_level is False
    assert sensor_data.potassium_level is False
    assert sensor_data.ph_level == 0.0
    assert sensor_data.soil_moisture == 0.0
    assert sensor_data.irrigation_active is False 