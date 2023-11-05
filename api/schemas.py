
#api/schemas.py

from pydantic import BaseModel, UUID4

class UserCreate(BaseModel):
    email: str
    password: str
    username: str

class UserOut(BaseModel):
    uuid: UUID4  # UUIDフィールドを追加
    email: str
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

class TokenData(BaseModel):
    user_id: str

#変更
# # api/schemas.py

# from pydantic import BaseModel, UUID4

# class UserCreate(BaseModel):
#     email: str
#     password: str
#     username: str

# class UserOut(BaseModel):
#     uuid: UUID4  # UUIDフィールドを追加
#     email: str
#     username: str

#     class Config:
#         orm_mode = True

# class UserLogin(BaseModel):
#     username: str
#     email: str
#     password: str

# class Token(BaseModel):
#     access_token: str
#     token_type: str