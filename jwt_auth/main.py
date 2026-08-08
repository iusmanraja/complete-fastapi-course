from fastapi import FastAPI, Depends

from database import engine, Base

from models import User

from dependencies import get_current_user

from auth import router as auth_router


app = FastAPI()


Base.metadata.create_all(bind=engine)


app.include_router(auth_router)


@app.get("/profile")
def profile(current_user: User = Depends(get_current_user)):
    return current_user