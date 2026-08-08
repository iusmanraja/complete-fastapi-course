from fastapi import Depends, HTTPException, status

from fastapi.security import OAuth2PasswordBearer

from sqlalchemy.orm import Session

from database import get_db

from models import User, RevokedToken

from utils import decode_access_token



oauth2_scheme= OAuth2PasswordBearer(tokenUrl="/auth/login")



def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    payload = decode_access_token(token)

    if payload is None:
        raise HTTPException(status_code=401, detail="Invalid Token")

    revoked_token = db.query(RevokedToken).filter(RevokedToken.token == token).first()

    if revoked_token:
        raise HTTPException(status_code=401,detail="Token has been revoked")

    email = payload.get("sub")

    current_user = db.query(User).filter(User.email == email).first()

    if not current_user:
        raise HTTPException(status_code=404, detail="User Not Found")

    return current_user