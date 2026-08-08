from passlib.context import CryptContext

from datetime import datetime, timedelta, timezone

from jose import jwt, JWTError

from dotenv import load_dotenv
import os

load_dotenv()


SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES"))
REFRESH_TOKEN_EXPIRE_DAYS = int(os.getenv("REFRESH_TOKEN_EXPIRE_DAYS"))



pwd_context = CryptContext(
    schemes=["bcrypt"],
    deprecated="auto"
)




def hash_password(password: str) -> str:
    return pwd_context.hash(password)




def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)




def create_access_token(data: dict) -> str:
    to_encode = data.copy()
    
    expire =  datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)

    to_encode.update({"exp": expire})

    token = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

    return token




def decode_access_token(token: str) -> dict | None:
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])

        return payload
        
    except JWTError:
        return None




def create_refresh_token(data: dict) -> str:
    to_encode = data.copy()

    expire = datetime.now(timezone.utc) + timedelta(days=REFRESH_TOKEN_EXPIRE_DAYS)

    to_encode.update({"exp": expire, "type": "refresh"})

    token = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

    return token




def decode_refresh_token(token: str) -> dict | None:
    try:
        payload = jwt.decode(token,SECRET_KEY,algorithms=[ALGORITHM])

        if payload.get("type") != "refresh":
            return None

        return payload

    except JWTError:
        return None


