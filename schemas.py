from pydantic import BaseModel, Field


class User(BaseModel):
    id: int
    name: str
    username: str = Field(..., description="Username cannot be NULL")
    password: str

    # class Config:
    #     orm_mode = True


class UserCreate(BaseModel):
    id:int
    name: str
    username: str = Field(..., description="Numele de utilizator, nu poate fi NULL")
    password: str

    # class Config:
    #     orm_mode = True

class URLCreate(BaseModel):
    id: int = Field(..., description="ID of the URL")
    long_url: str = Field(..., description="The long URL to be shortened")
    short_url: str = Field(..., description="The shortened URL")
    user_id: int

    # class Config:
    #     orm_mode = True