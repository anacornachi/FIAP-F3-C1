import pytest
from datetime import datetime, timedelta

from ..database.models.sensor_data import SensorData

def test_process_sensor_data_irrigation_activation(sensor_service):
    # Caso 1: Umidade muito baixa
    data1 = SensorData(soil_moisture=20.0)
    processed1 = sensor_service.process_sensor_data(data1)
    assert processed1.irrigation_active is True

    # Caso 2: pH fora do ideal
    data2 = SensorData(ph_level=4.0)
    processed2 = sensor_service.process_sensor_data(data2)
    assert processed2.irrigation_active is True

    # Caso 3: Falta de fósforo
    data3 = SensorData(phosphorus_level=False)
    processed3 = sensor_service.process_sensor_data(data3)
    assert processed3.irrigation_active is True

    # Caso 4: Falta de potássio
    data4 = SensorData(potassium_level=False)
    processed4 = sensor_service.process_sensor_data(data4)
    assert processed4.irrigation_active is True

def test_process_sensor_data_no_irrigation(sensor_service):
    data = SensorData(
        phosphorus_level=True,
        potassium_level=True,
        ph_level=6.5,
        soil_moisture=45.0
    )
    processed = sensor_service.process_sensor_data(data)
    assert processed.irrigation_active is False

def test_get_sensor_statistics(sensor_service):
    # Criar dados de teste
    now = datetime.now()
    test_data = [
        SensorData(
            timestamp=now - timedelta(hours=i),
            phosphorus_level=i % 2 == 0,  # Alterna entre True e False
            potassium_level=i % 3 == 0,   # True a cada 3 registros
            ph_level=6.0 + (i * 0.1),    # pH varia de 6.0 a 6.9
            soil_moisture=40.0 + i,       # Umidade varia de 40.0 a 49.0
            irrigation_active=i % 2 == 0  # Alterna entre True e False
        )
        for i in range(10)
    ]
    
    # Inserir dados
    for data in test_data:
        sensor_service.process_sensor_data(data)
    
    # Calcular estatísticas
    stats = sensor_service.get_sensor_statistics(
        now - timedelta(hours=10),
        now
    )
    
    # Verificar estatísticas
    assert 'average_ph' in stats
    assert 'average_moisture' in stats
    assert 'irrigation_time_percentage' in stats
    assert 'phosphorus_deficiency_percentage' in stats
    assert 'potassium_deficiency_percentage' in stats
    
    # Verificar valores específicos
    assert 6.0 <= stats['average_ph'] <= 6.9
    assert 40.0 <= stats['average_moisture'] <= 49.0
    assert stats['irrigation_time_percentage'] == 50.0  # 5 de 10 registros
    assert stats['phosphorus_deficiency_percentage'] == 50.0  # 5 de 10 registros
    assert 30.0 <= stats['potassium_deficiency_percentage'] <= 40.0  # 3-4 de 10 registros

def test_crud_operations(sensor_service):
    # Create
    data = SensorData(
        phosphorus_level=True,
        potassium_level=True,
        ph_level=6.5,
        soil_moisture=45.0
    )
    created = sensor_service.process_sensor_data(data)
    assert created.id is not None
    
    # Read
    retrieved = sensor_service.get_sensor_data(created.id)
    assert retrieved is not None
    assert retrieved.id == created.id
    
    # Update
    retrieved.ph_level = 7.0
    updated = sensor_service.update_sensor_data(retrieved)
    assert updated is not None
    assert updated.ph_level == 7.0
    
    # Delete
    assert sensor_service.delete_sensor_data(created.id) is True
    assert sensor_service.get_sensor_data(created.id) is None 