from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from . import crud, models, schemas, database
from .database import SessionLocal, engine
from fastapi.middleware.cors import CORSMiddleware
from fastapi import status
from datetime import timedelta
from .auth import authenticate_user, create_access_token
import uuid  # UUIDを生成するために追加


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
    # Emailがすでに登録されているか確認
    db_user = crud.get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    # UUIDを生成
    user_id = str(uuid.uuid4())
    # CRUD関数を使ってユーザーを作成
    return crud.create_user(db=db, user=user, uuid=user_id)

# @app.post("/login", response_model=schemas.Token)
@app.post("/login", response_model=schemas.Token)
def login(user_login: schemas.UserLogin, db: Session = Depends(get_db)):
    user = crud.authenticate_user(db, user_login.username, user_login.email, user_login.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect login details",
            headers={"WWW-Authenticate": "Bearer"},
        )
    # トークン生成時にUUIDを使用
    access_token_expires = timedelta(days=10000)  # 有効期限は適切な値に設定
    access_token = create_access_token(
        data={"sub": str(user.uuid)}, expires_delta=access_token_expires
    )

    response = schemas.Token
    response.access_token = access_token
    response.token_type = "bearer"

    return response

# テスト用のHello Worldエンドポイント
@app.get("/hello")
def read_root():
    return {"message": "Hello World"}
