from typing import List, Optional
from database.oracle import db
from database.models import ClimateData
from datetime import datetime

def create_climate_data(data: dict) -> dict:
    climate = ClimateData(
        timestamp=data.get("timestamp", datetime.utcnow()),
        temperature=data["temperature"],
        air_humidity=data["air_humidity"],
        rain_forecast=data["rain_forecast"]
    )
    db.session.add(climate)
    db.session.commit()
    db.session.refresh(climate)
    return climate.to_dict()


def get_climate_data(climate_id: str) -> Optional[dict]:
    climate = db.session.query(ClimateData).filter_by(id=climate_id).first()
    if climate:
        return climate.to_dict()
    return None


def list_climate_data() -> List[dict]:
    climates = db.session.query(ClimateData).order_by(ClimateData.timestamp.desc()).all()
    return [c.to_dict() for c in climates]


def update_climate_data(climate_id: str, data: dict) -> Optional[dict]:
    climate = db.session.query(ClimateData).filter_by(id=climate_id).first()
    if not climate:
        return None

    if "temperature" in data:
        climate.temperature = data["temperature"]
    if "air_humidity" in data:
        climate.air_humidity = data["air_humidity"]
    if "rain_forecast" in data:
        climate.rain_forecast = data["rain_forecast"]
    if "timestamp" in data:
        climate.timestamp = data["timestamp"]

    db.session.commit()
    db.session.refresh(climate)
    return climate.to_dict()


def delete_climate_data(climate_id: str) -> bool:
    climate = db.session.query(ClimateData).filter_by(id=climate_id).first()
    if not climate:
        return False
    db.session.delete(climate)
    db.session.commit()
    return True
