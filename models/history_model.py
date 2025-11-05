from sqlalchemy import Column, Integer, String, Float, DateTime, func
from database import Base

class WeatherHistory(Base):
    __tablename__ = "weather_history"

    id = Column(Integer, primary_key=True, index=True)
    city_name = Column(String(100), nullable=False)
    temperature = Column(Float)
    weather_desc = Column(String(255))
    humidity = Column(Integer)
    wind_speed = Column(Float)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
