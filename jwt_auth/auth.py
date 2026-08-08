from fastapi import APIRouter, Depends, HTTPException, status

from sqlalchemy.orm import Session

from datetime import datetime, timezone

from models import User, RevokedToken

from utils import hash_password, verify_password

from schemas import UserCreate,UserResponse, Token, RefreshTokenRequest

from database import get_db

from utils import (
    create_access_token,
    create_refresh_token,
    decode_access_token,
    decode_refresh_token
)

from dependencies import get_current_user, oauth2_scheme

from fastapi.security import OAuth2PasswordRequestForm



router = APIRouter(
    prefix="/auth",
    tags=["Authentication"]
)


@router.post("/register", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def register(user: UserCreate, db : Session = Depends(get_db)):
    existing_user = db.query(User).filter(User.email == user.email).first()
    if existing_user:
        raise HTTPException(status_code= 400, detail="Email Already Exist")

    hashed_password = hash_password(user.password)

    new_user = User(name= user.name, email= user.email, hashed_password=hashed_password)

    db.add(new_user)
    db.commit()
    db.refresh(new_user)


    return new_user



@router.post("/login",  response_model=Token)
async def login(form_data: OAuth2PasswordRequestForm = Depends(),db: Session = Depends(get_db)):

    db_user = db.query(User).filter(User.email == form_data.username).first()

    if not db_user:
        raise HTTPException(status_code=404,detail="User Not Found")

    password_valid = verify_password(form_data.password,db_user.hashed_password)

    if not password_valid:
        raise HTTPException(status_code=400,detail="Invalid Password")

    access_token = create_access_token(data={"sub": db_user.email})
    refresh_token = create_refresh_token(data={"sub": db_user.email})
    return {
        "access_token": access_token,
        "refresh_token": refresh_token,
        "token_type": "bearer"
    }




@router.post("/refresh", response_model=Token)
async def refresh_token(data: RefreshTokenRequest, db: Session = Depends(get_db)):
    
    payload = decode_refresh_token(data.refresh_token)

    if payload is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or Expired Refresh Token"
        )


    email = payload.get("sub")

    if not email:
        raise HTTPException(status_code=400,detail="Invalid Email")


    db_user = db.query(User).filter(User.email == email).first()

    if not db_user:
        raise HTTPException(status_code=404,detail="User Not Found")

        
    access_token = create_access_token(data={"sub": db_user.email})

    return{
        "access_token": access_token,
        "refresh_token": data.refresh_token,
        "token_type": "bearer"
    }



@router.post("/logout")
async def logout(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    payload = decode_access_token(token)

    if payload is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="Invalid or Expired Token")

    expire_at = payload.get("exp")

    if expire_at is None:
        raise HTTPException(status_code=400,detail="Token Expiry Missing")
        
    expires_at = datetime.fromtimestamp(expire_at, tz=timezone.utc)

    revoked_token = RevokedToken(token=token,expires_at=expires_at)


    db.add(revoked_token)
    db.commit()

    return{
        "message": "Logout Successfully"
    }
    

    





@router.get("/users/me")
async def get_me(current_user: User = Depends(get_current_user)):
    return current_user
