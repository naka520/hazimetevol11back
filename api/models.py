from sqlalchemy import Column, Integer, String
from sqlalchemy.dialects.postgresql import UUID
import uuid
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class User(Base):
    __tablename__ = 'users'  # tablename が正しい属性名です

    id = Column(Integer, primary_key=True, index=True)
    uuid = Column(String(36), unique=True, index=True, default=lambda: str(uuid.uuid4()))  # UUIDを文字列として保存
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    username = Column(String)