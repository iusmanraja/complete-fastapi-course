from pydantic import BaseModel, EmailStr, Field

from pydantic import ConfigDict



class UserCreate(BaseModel):
    name: str = Field(min_length=3, max_length=20)
    email: EmailStr
    password: str = Field(min_length=4)


class UserLogin(BaseModel):
    email: EmailStr
    password: str = Field(min_length=4)
    

class UserResponse(BaseModel):
    id: int = Field(ge=1)
    name: str = Field(min_length=3, max_length=20)
    email: EmailStr

    model_config = ConfigDict(from_attributes=True)


class Token(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str


class RefreshTokenRequest(BaseModel):
    refresh_token: str

