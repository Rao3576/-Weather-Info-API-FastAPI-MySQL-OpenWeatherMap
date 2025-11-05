from fastapi import FastAPI
from routers import weather_router
from database import Base, engine
from models import history_model  # ensures models are loaded

# ✅ Create tables automatically if not exist
Base.metadata.create_all(bind=engine)

app = FastAPI(title="Weather Info API")

# Include router
app.include_router(weather_router.router)

@app.get("/")
def home():
    return {"message": "🌦️ Welcome to the Weather Info API"}

