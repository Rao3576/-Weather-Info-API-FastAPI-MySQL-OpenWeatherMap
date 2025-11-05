# -Weather-Info-API-FastAPI-MySQL-OpenWeatherMap
A simple yet powerful FastAPI project that fetches real-time weather data using the OpenWeatherMap API and stores it into a MySQL database.




---

## 🚀 Project Overview

This project demonstrates how to build a complete **FastAPI + MySQL** application that:
- Fetches **live weather information** using the OpenWeatherMap API.
- Stores each weather request in a **database table** for history tracking.
- Provides REST API endpoints to **view live weather** and **check past history**.

---

## 🧩 Tech Stack

| Component | Technology Used |
|------------|-----------------|
| Backend Framework | 🧠 FastAPI |
| Database | 🗄️ MySQL (with SQLAlchemy ORM) |
| HTTP Client | 🌐 Requests |
| Environment Management | ⚙️ python-dotenv |
| Language | 🐍 Python 3.10+ |

---

## 📁 Project Structure

```

Weather-Info-API--FastAPI-MySQL/
│
├── main.py                          # Main FastAPI entry point
├── database.py                      # DB connection & session
├── models/
│   └── history_model.py             # WeatherHistory database model
├── routers/
│   └── weather_router.py            # API endpoints (fetch & history)
├── utils/
│   └── weather_service.py           # OpenWeatherMap API integration
├── .env                             # Contains API key & DB credentials
├── requirements.txt                 # All required libraries
└── README.md                        # This file 😄

````

---

## ⚙️ Setup Instructions

### 1️⃣ Clone the Repository
```bash
git clone https://github.com/YOUR_USERNAME/Weather-Info-API--FastAPI-MySQL.git
cd Weather-Info-API--FastAPI-MySQL
````

### 2️⃣ Create a Virtual Environment

```bash
python -m venv venv
venv\Scripts\activate   # For Windows
# or
source venv/bin/activate  # For Mac/Linux
```

### 3️⃣ Install Requirements

```bash
pip install -r requirements.txt
```

### 4️⃣ Setup `.env` File

Create a `.env` file in the root directory:

```
OPENWEATHER_API_KEY=YOUR_API_KEY
DB_USER=root
DB_PASSWORD=yourpassword
DB_HOST=localhost
DB_NAME=wheather_db
```

> 🧠 Tip: You can get your free API key from [https://openweathermap.org/api](https://openweathermap.org/api)

---

## 🛠️ Run the Application

```bash
uvicorn main:app --reload
```

Now visit: 👉 **[http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)**

You’ll see a Swagger UI (interactive documentation) with two main endpoints:

1. `/weather/` → Fetch current weather by city name
2. `/weather/history` → Retrieve all previously fetched weather data

---

## 🌐 How It Works — Step by Step

1. User sends request → `/weather/?city=Lahore`
2. FastAPI calls OpenWeatherMap API using the city name.
3. Weather data (temp, humidity, etc.) is fetched live.
4. Data is saved in **MySQL** under `weather_history` table.
5. Response is sent back with the current weather info.
6. You can later view saved records via `/weather/history`.

---

## 🧠 Example API Response

**GET /weather/?city=Lahore**

```json
{
  "message": "✅ Weather fetched successfully",
  "data": {
    "city_name": "Lahore",
    "temperature": 19.5,
    "weather_desc": "clear sky",
    "humidity": 56,
    "wind_speed": 2.5
  }
}
```

**GET /weather/history**

```json
{
  "count": 3,
  "data": [
    {
      "city_name": "Lahore",
      "temperature": 19.5,
      "weather_desc": "clear sky",
      "humidity": 56,
      "wind_speed": 2.5
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

## 🧰 Key Files Explained

### 🔸 `main.py`

Starts the FastAPI app and registers the routes.

```python
from fastapi import FastAPI
from routers import weather_router

app = FastAPI(title="Weather Info API")

app.include_router(weather_router.router)

@app.get("/")
def home():
    return {"message": "🌦️ Welcome to the Weather Info API"}
```

---

### 🔸 `weather_router.py`

Handles API routes — fetching live weather and showing history.

```python
@router.get("/")
def fetch_weather(city: str, db: Session = Depends(get_db)):
    weather = get_weather_data(city)
    record = WeatherHistory(**weather)
    db.add(record)
    db.commit()
    return {"message": "✅ Weather fetched successfully", "data": weather}
```

---

### 🔸 `weather_service.py`

Connects with the OpenWeatherMap API.

```python
response = requests.get(
    "https://api.openweathermap.org/data/2.5/weather",
    params={"q": city_name, "appid": API_KEY, "units": "metric"}
)
```

---

### 🔸 `history_model.py`

Defines the database table for storing history.

```python
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

---

## 🌈 Why This Project?

This project is a **beginner-friendly** example to learn:

* FastAPI Routing & Dependency Injection
* SQLAlchemy ORM integration
* Using `.env` and `requests` for external APIs
* How to connect APIs with databases in real time

---

## 🧡 Author

**Muhammad Kashif Mushtaq**


