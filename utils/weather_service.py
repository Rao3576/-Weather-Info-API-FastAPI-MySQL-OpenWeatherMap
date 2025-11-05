import requests
import os
from fastapi import HTTPException
from dotenv import load_dotenv

load_dotenv()  # Load .env values

# ✅ OpenWeatherMap API key (you must add this to your .env file)
API_KEY = "4c198d30a4f3e77df67baf2eac4db609"


if not API_KEY:
    raise ValueError("⚠️ Missing OPENWEATHER_API_KEY in .env file")

BASE_URL = "https://api.openweathermap.org/data/2.5/weather"


def get_weather_data(city_name: str):
    """
    Fetch weather data from OpenWeatherMap API for the given city.
    """
    params = {
        "q": city_name,
        "appid": API_KEY,
        "units": "metric"  # temperature in Celsius
    }

    try:
        response = requests.get(BASE_URL, params=params)
        data = response.json()

        # If city not found or error
        if response.status_code != 200:
            raise HTTPException(
                status_code=response.status_code,
                detail=data.get("message", "Error fetching weather data"),
            )

        # Extract useful info
        weather_info = {
            "city_name": data["name"],
            "temperature": data["main"]["temp"],
            "weather_desc": data["weather"][0]["description"],
            "humidity": data["main"]["humidity"],
            "wind_speed": data["wind"]["speed"],
        }

        return weather_info

    except requests.exceptions.RequestException as e:
        raise HTTPException(status_code=500, detail=f"Request error: {str(e)}")
