from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from . import crud, models, schemas, database
from .database import SessionLocal, engine
from fastapi.middleware.cors import CORSMiddleware
from fastapi import status
from datetime import timedelta
from .auth import authenticate_user, create_access_token


# DBモデルをDBに作成する（実運用ではAlembicなどのマイグレーションツールを使用）
models.Base.metadata.create_all(bind=engine)

app = FastAPI()

# CORS設定
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 全てのオリジンを許可
    allow_credentials=True,
    allow_methods=["*"],  # 全てのメソッドを許可
    allow_headers=["*"],  # 全てのヘッダーを許可
)

# DBセッションの依存関係
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# ユーザーの作成
@app.post("/users/", response_model=schemas.UserOut)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    if crud.get_user_by_email(db, email=user.email):
        raise HTTPException(status_code=400, detail="Email already registered")
    return crud.create_user(db=db, user=user)

@app.post("/login", response_model=schemas.Token)
def login(user_login: schemas.UserLogin, db: Session = Depends(get_db)):
    user = crud.authenticate_user(db, user_login.username, user_login.email, user_login.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect login details",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(days=10000)
    access_token = create_access_token(
        data={"sub": user.email}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}

# テスト用のHello Worldエンドポイント
@app.get("/hello")
def read_root():
    return {"message": "Hello World"}
