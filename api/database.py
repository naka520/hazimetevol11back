from typing import Generator
from sqlalchemy import create_engine, MetaData
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.session import Session
import os
import dotenv

dotenv.load_dotenv()


POSTGRES_USER = os.environ["POSTGRES_USER"]
POSTGRES_PASSWORD = os.environ["POSTGRES_PASSWORD"]
POSTGRES_HOST = os.environ["POSTGRES_HOST"]
POSTGRES_PORT = os.environ["POSTGRES_PORT"]
POSTGRES_DB = os.environ["POSTGRES_DB"]

uri = 'postgresql://{}:{}@{}:{}/{}'.format(POSTGRES_USER, POSTGRES_PASSWORD, POSTGRES_HOST, POSTGRES_PORT, POSTGRES_DB)
engine = create_engine(uri, pool_recycle=3600)
SessionLocal = sessionmaker(autocommit=False, autoflush=True, expire_on_commit=False, bind=engine)


def get_db() -> Generator[Session, None, None]:
    db_session: Session | None = None
    try:
        db_session = SessionLocal()
        yield db_session
    finally:
        if db_session is not None:
            db_session.close()
