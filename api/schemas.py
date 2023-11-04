# api/schemas.py

from pydantic import BaseModel

class UserCreate(BaseModel):
    email: str
    password: str
    username: str

class UserOut(BaseModel):
    id: int
    email: str
    username: str

    class Config:
        orm_mode = True
