# -Weather-Info-API-FastAPI-MySQL-OpenWeatherMap
A simple yet powerful FastAPI project that fetches real-time weather data using the OpenWeatherMap API and stores it into a MySQL database.


---

## 💡 What This Project Teaches

This project helps beginners learn:

* How **FastAPI routes** work
* How to connect **FastAPI with a MySQL database** using **SQLAlchemy**
* How to use **external REST APIs** (OpenWeatherMap)
* How to save and retrieve data using ORM models
* How to use **`.env`** files for secret keys and credentials

---

## 🧠 How the App Works (Simple Flow)

```
User → FastAPI Route (/weather) → OpenWeatherMap API → Response → Save to MySQL → Back to User
```

### Step-by-Step Flow:

1. The user sends a GET request like:
   `http://127.0.0.1:8000/weather/?city=Lahore`

2. The app calls OpenWeatherMap’s API to get live data for Lahore.

3. FastAPI receives that data and saves it in a MySQL table.

4. The API returns a response with temperature, humidity, and description.

5. All fetched cities are stored in a table called `weather_history`.

6. You can later check your saved history at `/weather/history`.

---

## 🧩 Tech Stack

| Purpose                | Tool Used        |
| ---------------------- | ---------------- |
| Framework              | 🧠 FastAPI       |
| Database               | 🗄️ MySQL        |
| ORM                    | 🧱 SQLAlchemy    |
| HTTP Requests          | 🌐 Requests      |
| Environment Management | ⚙️ python-dotenv |
| Language               | 🐍 Python 3.10+  |

---

## 📁 Folder Structure

```
Weather-Info-API--FastAPI-MySQL/
│
├── main.py                        # Entry point of the FastAPI app
├── database.py                    # Creates DB engine and session
├── models/
│   └── history_model.py           # Defines WeatherHistory table
├── routers/
│   └── weather_router.py          # Handles API routes
├── utils/
│   └── weather_service.py         # Connects to OpenWeatherMap API
├── .env                           # Holds API key and DB credentials
├── requirements.txt               # Required libraries
└── README.md                      # This file
```

---

## ⚙️ Setup Guide

### 1️⃣ Clone the Repository

```bash
git clone https://github.com/YOUR_USERNAME/Weather-Info-API--FastAPI-MySQL.git
cd Weather-Info-API--FastAPI-MySQL
```

### 2️⃣ Create Virtual Environment

```bash
python -m venv venv
venv\Scripts\activate      # Windows
# or
source venv/bin/activate   # macOS/Linux
```

### 3️⃣ Install Required Packages

```bash
pip install -r requirements.txt
```

### 4️⃣ Create `.env` File

```ini
OPENWEATHER_API_KEY=your_api_key_here
DB_USER=root
DB_PASSWORD=yourpassword
DB_HOST=localhost
DB_NAME=wheather_db
```

> You can get a free API key from [OpenWeatherMap](https://openweathermap.org/api)

---

## 🧰 Code Explanation (for Beginners)

Let’s understand the **main parts** of this project:

---

### 🔹 1. `main.py`

This is where the app starts.

```python
from fastapi import FastAPI
from routers import weather_router

app = FastAPI(title="Weather Info API")

# Include routes from weather_router.py
app.include_router(weather_router.router)

@app.get("/")
def home():
    return {"message": "🌦️ Welcome to the Weather Info API"}
```

**👉 Explanation:**

* `FastAPI()` creates your web application.
* `include_router()` connects routes from another file.
* The `/` route just shows a welcome message when you open the app.

---

### 🔹 2. `weather_router.py`

Handles both fetching live weather and retrieving saved history.

```python
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from database import get_db
from models.history_model import WeatherHistory
from utils.weather_service import get_weather_data

router = APIRouter(prefix="/weather", tags=["Weather"])

@router.get("/")
def fetch_weather(city: str = Query(..., description="Enter city name"), db: Session = Depends(get_db)):
    weather = get_weather_data(city)
    if not weather:
        raise HTTPException(status_code=404, detail="City not found or API error")

    # Save data into database
    record = WeatherHistory(
        city_name=weather["city_name"],
        temperature=weather["temperature"],
        weather_desc=weather["weather_desc"],
        humidity=weather["humidity"],
        wind_speed=weather["wind_speed"]
    )
    db.add(record)
    db.commit()

    return {"message": "✅ Weather fetched successfully", "data": weather}
```

**👉 Explanation:**

1. `@router.get("/")` — defines a GET endpoint `/weather/`.
2. `city` is taken from the user query.
3. `get_weather_data(city)` — fetches real-time weather from OpenWeatherMap.
4. Data is saved to MySQL (`WeatherHistory` table).
5. A success message + weather data is returned to the user.

---

### 🔹 3. `weather_service.py`

This file handles external API calls.

```python
import requests, os
from dotenv import load_dotenv

load_dotenv()
API_KEY = os.getenv("OPENWEATHER_API_KEY")
BASE_URL = "https://api.openweathermap.org/data/2.5/weather"

def get_weather_data(city_name: str):
    params = {"q": city_name, "appid": API_KEY, "units": "metric"}
    response = requests.get(BASE_URL, params=params)
    data = response.json()
    if response.status_code != 200:
        return None
    return {
        "city_name": data["name"],
        "temperature": data["main"]["temp"],
        "weather_desc": data["weather"][0]["description"],
        "humidity": data["main"]["humidity"],
        "wind_speed": data["wind"]["speed"],
    }
```

**👉 Explanation:**

* Uses `requests` to call the **OpenWeatherMap API**.
* Converts JSON data into a Python dictionary.
* Returns only the useful fields (city, temp, humidity, etc.).

---

### 🔹 4. `history_model.py`

Defines how data is stored in the database.

```python
from sqlalchemy import Column, Integer, String, Float, DateTime
from datetime import datetime
from database import Base

class WeatherHistory(Base):
    __tablename__ = "weather_history"
    id = Column(Integer, primary_key=True, index=True)
    city_name = Column(String(50))
    temperature = Column(Float)
    weather_desc = Column(String(100))
    humidity = Column(Integer)
    wind_speed = Column(Float)
    created_at = Column(DateTime, default=datetime.utcnow)
```

**👉 Explanation:**
Each time you call `/weather/`, one new record is inserted here.
The `created_at` column automatically saves the current timestamp.

---

## 🧠 Example API Usage

### 1️⃣ Fetch Live Weather

```
GET /weather/?city=Lahore
```

**Response:**

```json
{
  "message": "✅ Weather fetched successfully",
  "data": {
    "city_name": "Lahore",
    "temperature": 18.9,
    "weather_desc": "clear sky",
    "humidity": 60,
    "wind_speed": 2.3
  }
}
```

### 2️⃣ View Weather History

```
GET /weather/history
```

**Response:**

```json
{
  "count": 3,
  "data": [
    {
      "city_name": "Lahore",
      "temperature": 18.9,
      "weather_desc": "clear sky",
      "humidity": 60,
      "wind_speed": 2.3
    },
    {
      "city_name": "Karachi",
      "temperature": 29.2,
      "weather_desc": "smoke",
      "humidity": 70,
      "wind_speed": 3.0
    }
  ]
}
```

---

## 📊 Database Table Example

| id | city_name | temperature | weather_desc | humidity | wind_speed | created_at          |
| -- | --------- | ----------- | ------------ | -------- | ---------- | ------------------- |
| 1  | Lahore    | 18.9        | clear sky    | 60       | 2.3        | 2025-11-05 07:42:00 |
| 2  | Karachi   | 29.2        | smoke        | 70       | 3.0        | 2025-11-05 07:48:00 |

---

## 🧡 Author

**Muhammad Kashif Mushtaq**
