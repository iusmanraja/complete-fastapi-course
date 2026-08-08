from fastapi import FastAPI
from user import router

app = FastAPI()

app.include_router(router)