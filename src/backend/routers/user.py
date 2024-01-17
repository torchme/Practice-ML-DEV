from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from src.backend.models import UserCreate, UserOut
from src.db.crud.users import (
    add_user,
    get_user_by_username,
    verify_password,
    increment_user_balance,
    decrement_user_balance,
)
from src.db.database import get_db

user_router = APIRouter()


@user_router.post("/signup", response_model=UserOut)
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    existing_user = get_user_by_username(db, username=user.username)
    if existing_user:
        raise HTTPException(status_code=400, detail="Username already taken")

    db_user = add_user(db, user.username, user.password)
    return UserOut.from_orm(db_user)


@user_router.get("/signin", response_model=UserOut)
def read_user(username: str, password: str, db: Session = Depends(get_db)):
    db_user = get_user_by_username(db, username)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    elif not verify_password(password, db_user.hashed_password):
        raise HTTPException(status_code=401, detail="Incorrect password")
    return UserOut(id=db_user.id, username=db_user.username, balance=db_user.balance)


@user_router.post("/increment_balance")
def add_balance(username: str, amount: float, db: Session = Depends(get_db)):
    updated_user = increment_user_balance(db, username, amount)
    return UserOut(
        id=updated_user.id, username=updated_user.username, balance=updated_user.balance
    )


@user_router.post("/decrement_balance")
def subtract_balance(username: str, amount: float, db: Session = Depends(get_db)):
    updated_user = decrement_user_balance(db, username, amount)
    return UserOut(
        id=updated_user.id, username=updated_user.username, balance=updated_user.balance
    )
