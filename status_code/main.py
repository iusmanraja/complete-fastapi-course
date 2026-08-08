from fastapi import FastAPI, status

app = FastAPI()


@app.post("/users", status_code=status.HTTP_201_CREATED)
async def create_user():
    return {"message": "User created successfully"}


@app.get("/users/{user_id}", status_code=status.HTTP_200_OK)
async def get_user(user_id: int):
    return {
        "message": "User fetched successfully",
        "user_id": user_id
    }

@app.put("/users/{user_id}", status_code=status.HTTP_200_OK)
async def updated_user(user_id: int):
    return{
        "message": "User updated successfully"
    }


@app.delete("/users/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
async def deleted_user(user_id: int):
    return{
        "message": "User deleted successfully"
    }