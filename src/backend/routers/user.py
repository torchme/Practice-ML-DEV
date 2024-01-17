from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from src.backend.models import UserCreate, UserOut, UserWithToken
from src.db.crud.users import (
    add_user,
    get_user_by_username,
    verify_password,
    increment_user_balance,
    decrement_user_balance,
)
from src.db.database import get_db
from src.backend.dependencies import create_access_token, get_current_user


user_router = APIRouter()


@user_router.post("/signup", response_model=UserWithToken)
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    existing_user = get_user_by_username(db, username=user.username)
    if existing_user:
        raise HTTPException(status_code=400, detail="Username already taken")
    db_user = add_user(db, user.username, user.password)
    access_token = create_access_token(data={"sub": db_user.username})
    return {
        "user": UserOut.from_orm(db_user),
        "access_token": access_token,
        "token_type": "bearer",
    }


@user_router.get("/signin", response_model=UserWithToken)
def read_user(username: str, password: str, db: Session = Depends(get_db)):
    db_user = get_user_by_username(db, username)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    elif not verify_password(password, db_user.hashed_password):
        raise HTTPException(status_code=401, detail="Incorrect password")
    access_token = create_access_token(data={"sub": db_user.username})
    return {
        "access_token": access_token,
        "token_type": "bearer",
        "user": UserOut(
            id=db_user.id, username=db_user.username, balance=db_user.balance
        ),
    }


@user_router.post("/increment_balance")
def add_balance(
    amount: float,
    db: Session = Depends(get_db),
    username: str = Depends(get_current_user),
):
    updated_user = increment_user_balance(db, username.username, amount)
    return UserOut(
        id=updated_user.id, username=updated_user.username, balance=updated_user.balance
    )


@user_router.post("/decrement_balance")
def subtract_balance(
    amount: float,
    db: Session = Depends(get_db),
    username: str = Depends(get_current_user),
):
    updated_user = decrement_user_balance(db, username.username, amount)
    return UserOut(
        id=updated_user.id, username=updated_user.username, balance=updated_user.balance
    )
