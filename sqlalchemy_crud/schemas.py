from pydantic import BaseModel, EmailStr, Field


class UserCreate(BaseModel):
    name: str = Field(min_length=3, max_length=50)
    email: EmailStr


class UserResponse(BaseModel):
    id: int = Field(ge=1)
    name: str = Field(min_length=3, max_length=50)
    email: EmailStr


class UserUpdate(BaseModel):
    name: str = Field(min_length=3, max_length=50)
    email: EmailStr
