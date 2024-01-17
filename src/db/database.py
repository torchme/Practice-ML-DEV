import os
import sys
import sqlalchemy as db
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base


PATH_DB = os.path.join(sys.path[0], "artifacts/db/healthcare.sqlite")
SQLALCHEMY_DATABASE_URL = f"sqlite:///{PATH_DB}"


engine = db.create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
