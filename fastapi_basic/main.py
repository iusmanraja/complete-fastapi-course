from fastapi import FastAPI
from hello_api import router

app = FastAPI()

app.include_router(router)