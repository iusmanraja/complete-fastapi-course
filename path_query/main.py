from fastapi import FastAPI, Path, Query
from schemas.user import User

app = FastAPI()
users = []

@app.post("/users")
async def create_user(user:User):
    users.append(user)
    return{
        "message": "User Created",
        "data": user
    }


@app.put("/users/{user_id}")
async def updated_user(
    user: User,
    user_id: int = Path(ge=0, description="User ID"),
    notify: bool = Query(
        default=False,
        description="Send notification"
    )
):
    if user_id < len(users):
        users[user_id] = user

        return {
            "message": "User Updated",
            "notify": notify,
            "data": user
        }