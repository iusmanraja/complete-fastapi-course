from fastapi import FastAPI
from schemas.user import UserResponse

app = FastAPI()

@app.get("/user", response_model=UserResponse)
async def get_user():
    return{
        "name": "Usman",
        "age": 20,
        "password": "11223344"
    }