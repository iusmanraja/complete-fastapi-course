from fastapi import FastAPI
from schemas.user import User

app = FastAPI()


@app.post("/users")
async def create_user(user: User):
    return{
        "message": "User created successfully",
        "user": user
    }