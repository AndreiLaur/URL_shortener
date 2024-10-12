from pydantic import BaseModel, Field

class UserCreate(BaseModel):
    id: int
    name: str
    username: str = Field(..., description="Numele de utilizator, nu poate fi NULL")
    password: str

    class Config:
        orm_mode = True

class URLCreate(BaseModel):
    id: int = Field(..., description="ID-ul URL-ului")
    long_url: str = Field(..., description="URL-ul lung, nu poate fi NULL")
    short_url: str = Field(..., description="URL-ul scurt, nu poate fi NULL")
    owner_id: int

    class Config:
        orm_mode = True
