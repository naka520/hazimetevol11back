# api/schemas.py

from pydantic import BaseModel, EmailStr, UUID4

class UserCreate(BaseModel):
    email: EmailStr
    password: str
    username: str

class UserOut(BaseModel):
    uuid: UUID4  # UUIDフィールドを追加
    email: EmailStr
    username: str

    class Config:
        orm_mode = True

class UserLogin(BaseModel):
    username: str
    email: str
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str