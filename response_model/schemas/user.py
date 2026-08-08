from pydantic import BaseModel, Field


class User(BaseModel):
    name:str = Field(min_length=3, max_length=30)
    age: int = Field(ge=18, le=60)
    password: str = Field(min_length=4)


class UserResponse(BaseModel):
    name:str = Field(min_length=3, max_length=30)
    age: int = Field(ge=18, le=60)

