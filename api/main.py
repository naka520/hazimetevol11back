from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from . import crud, models, schemas, database
from .database import SessionLocal, engine ,get_db
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
    access_token = create_access_token(user=user, expires_delta=access_token_expires)
    response = schemas.Token(access_token=access_token, token_type="bearer")
    return response 

# テスト用のHello Worldエンドポイント
@app.get("/hello")
def read_root():
    return {"message": "Hello World"}

#変更
# from fastapi import FastAPI, Depends, HTTPException
# import jwt
# from sqlalchemy.orm import Session
# from . import crud, models, schemas, database
# from .database import SessionLocal, engine
# from fastapi.middleware.cors import CORSMiddleware
# from fastapi import status
# from datetime import timedelta
# from .auth import authenticate_user, create_access_token
# import uuid  # UUIDを生成するために追加
# from fastapi import Security
# from fastapi.security import OAuth2PasswordBearer
# import jwt

# oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")
# SECRET_KEY = "a_very_secret_key"
# ALGORITHM = "HS256"


# # DBモデルをDBに作成する（実運用ではAlembicなどのマイグレーションツールを使用）
# models.Base.metadata.create_all(bind=engine)

# app = FastAPI()

# # CORS設定
# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=["*"],  # 全てのオリジンを許可
#     allow_credentials=True,
#     allow_methods=["*"],  # 全てのメソッドを許可
#     allow_headers=["*"],  # 全てのヘッダーを許可
# )

# # DBセッションの依存関係
# def get_db():
#     db = SessionLocal()
#     try:
#         yield db
#     finally:
#         db.close()

# # ユーザーの作成
# @app.post("/users/", response_model=schemas.UserOut)
# def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
#     # Emailがすでに登録されているか確認
#     db_user = crud.get_user_by_email(db, email=user.email)
#     if db_user:
#         raise HTTPException(status_code=400, detail="Email already registered")
#     # UUIDを生成
#     user_id = str(uuid.uuid4())
#     # CRUD関数を使ってユーザーを作成
#     return crud.create_user(db=db, user=user, uuid=user_id)

# # @app.post("/login", response_model=schemas.Token)
# @app.post("/login", response_model=schemas.Token)
# def login(user_login: schemas.UserLogin, db: Session = Depends(get_db)):
#     user = crud.authenticate_user(db, user_login.username, user_login.email, user_login.password)
#     if not user:
#         raise HTTPException(
#             status_code=status.HTTP_401_UNAUTHORIZED,
#             detail="Incorrect login details",
#             headers={"WWW-Authenticate": "Bearer"},
#         )
#     # トークン生成時にUUIDを使用
#     access_token_expires = timedelta(days=10000)  # 有効期限は適切な値に設定
#     access_token = create_access_token(user=user, expires_delta=access_token_expires)
#     response = schemas.Token(access_token=access_token, token_type="bearer")
#     return response 

# # テスト用のHello Worldエンドポイント
# @app.get("/hello")
# def read_root():
#     return {"message": "Hello World"}

# # ユーザー固有のUUIDを取得するエンドポイント
# @app.get("/get-my-uuid", response_model=schemas.UserUUID)  # response_modelをUserUUIDに変更する
# def get_my_uuid(token: str = Security(oauth2_scheme), db: Session = Depends(get_db)):
#     credentials_exception = HTTPException(
#         status_code=status.HTTP_401_UNAUTHORIZED,
#         detail="Could not validate credentials",
#         headers={"WWW-Authenticate": "Bearer"},
#     )
#     try:
#         payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
#         user_id = payload.get("sub")
#         if user_id is None:
#             raise credentials_exception
#         token_data = schemas.TokenData(user_id=user_id)  # TokenDataのインスタンスを作成
#     except jwt.PyJWTError:
#         raise credentials_exception

#     # CRUDメソッドでユーザーを取得
#     user = crud.get_user_by_uuid(db, uuid=user_id)  # UUIDを使用してユーザーを取得するためのCRUDメソッド
#     if user is None:
#         raise credentials_exception
#     return user  # UserUUIDのみを返すためにUserOutの代わりにUserUUIDスキーマを使用