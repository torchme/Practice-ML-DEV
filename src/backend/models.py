from pydantic import BaseModel


class UserCreate(BaseModel):
    username: str
    password: str


class UserOut(BaseModel):
    id: int
    username: str
    balance: int

    class Config:
        orm_mode = True


class UserWithToken(BaseModel):
    user: UserOut
    access_token: str
    token_type: str

    class Config:
        orm_mode = True


class UserWithItem(BaseModel):
    user: UserOut
    item: dict

    class Config:
        orm_mode = True


class Item(BaseModel):
    id: int
    owner_id: int

    class Config:
        orm_mode = True
