# api/auth.py

from datetime import datetime, timedelta
from jose import jwt
from passlib.context import CryptContext
from .models import User
from sqlalchemy.orm import Session

# トークン生成のための設定
SECRET_KEY = "a_very_secret_key"
ALGORITHM = "HS256"

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def authenticate_user(db: Session, username: str, email: str, password: str):
    # ユーザー名とメールでユーザーを見つけるためのクエリを追加
    user = db.query(User).filter(User.email == email, User.username == username).first()
    if not user:
        return False
    if not verify_password(password, user.hashed_password):
        return False
    return user

def create_access_token(user: User, expires_delta: timedelta = None):
    to_encode = {
        "sub": user.username,  # または user.email - トークンの主張(subject)にユーザー名またはメールを設定
        "user_uuid": str(user.uuid)  # ユーザーのUUIDをトークンに含める
    }
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(days=10000)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt
