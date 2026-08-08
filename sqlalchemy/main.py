from fastapi import FastAPI
from database import engine, Base
from models import User

app = FastAPI()

# Create Tables
Base.metadata.create_all(bind=engine)


@app.get("/")
def home():
    return {
        "message": "SQLAlchemy Connected Successfully"
    }