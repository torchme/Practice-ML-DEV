import src.db.core as core
from fastapi import HTTPException
from passlib.context import CryptContext
from sqlalchemy.orm import Session

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def get_password_hash(password):
    return pwd_context.hash(password)


def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


def add_user(db: Session, username: str, password: str):
    hashed_password = get_password_hash(password)
    db_user = core.User(username=username, hashed_password=hashed_password, balance=0)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def get_user_by_username(db: Session, username: str):
    return db.query(core.User).filter(core.User.username == username).first()


def increment_user_balance(db: Session, username: str, amount: float):
    user = db.query(core.User).filter(core.User.username == username).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    user.balance += amount
    db.commit()
    return user


def decrement_user_balance(db: Session, username: str, amount: float):
    user = db.query(core.User).filter(core.User.username == username).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    if user.balance < amount:
        raise HTTPException(status_code=400, detail="Insufficient balance")
    user.balance -= amount
    db.commit()
    return user
