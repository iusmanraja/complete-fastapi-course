from fastapi import FastAPI
from path import router

app = FastAPI()

app.include_router(router)