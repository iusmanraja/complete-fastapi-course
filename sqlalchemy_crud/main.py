from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db, engine, Base
from models import User
from schemas import UserCreate, UserResponse, UserUpdate
import models

Base.metadata.create_all(bind=engine)
app = FastAPI()



# Create User 
@app.post("/users", response_model=UserResponse)
async def create_user(user: UserCreate,db: Session = Depends(get_db)):
    new_user = User(name=user.name,email=user.email)

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user



# Get All Users 
@app.get("/users", response_model=list[UserResponse])
async def get_users(db: Session = Depends(get_db)):
    
    users = db.query(User).all()
    
    return users



# Get User By id 
@app.get("/users/{user_id}", response_model=UserResponse)
async def user_by_id(user_id: int, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()

    if not user:
        raise HTTPException(status_code=404, detail="User Not Found")

    return user



# Update User 
@app.put("/users/{user_id}", response_model=UserResponse)
async def update_user(user: UserUpdate, user_id: int, db: Session = Depends(get_db)):
    user_update = db.query(User).filter(User.id == user_id).first()

    if not user_update:
        raise HTTPException(status_code=404, detail="User Not Found")

    user_update.name = user.name
    user_update.email = user.email

    db.commit()
    db.refresh(user_update)

    return user_update


# Delete User 
@app.delete("/users/{user_id}", response_model=UserResponse)
async def delete_user(user_id: int, db: Session = Depends(get_db)):
    user_delete = db.query(User).filter(User.id == user_id).first()

    if not user_delete:
        raise HTTPException(status_code=404, detail="User Not Found")

    db.delete(user_delete)
    db.commit()

    return user_delete