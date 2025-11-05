from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from database import get_db
from models.history_model import WeatherHistory
from utils.weather_service import get_weather_data

router = APIRouter(prefix="/weather", tags=["Weather"])


@router.get("/")
def fetch_weather(city: str = Query(..., description="Enter city name"), db: Session = Depends(get_db)):
    """
    Fetch current weather info for a given city.
    - Retrieves data from OpenWeatherMap API
    - Saves result in database
    """

    # ✅ Fetch live data from OpenWeatherMap
    weather = get_weather_data(city)

    if not weather:
        raise HTTPException(status_code=404, detail="City not found or API error")

    # ✅ Store the result in DB
    record = WeatherHistory(
        city_name=weather["city_name"],
        temperature=weather["temperature"],
        weather_desc=weather["weather_desc"],
        humidity=weather["humidity"],
        wind_speed=weather["wind_speed"],
    )

    db.add(record)
    db.commit()
    db.refresh(record)

    return {
        "message": "✅ Weather fetched successfully",
        "data": weather
    }


@router.get("/history")
def get_weather_history(db: Session = Depends(get_db)):
    """
    Retrieve all saved weather history records.
    """
    records = db.query(WeatherHistory).order_by(WeatherHistory.created_at.desc()).all()

    if not records:
        return {"message": "No history records found"}

    return {"count": len(records), "data": records}
