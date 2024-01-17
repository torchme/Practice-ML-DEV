from sqlalchemy import Column, Float, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from .database import Base


class User(Base):
    "User class of creating db table"

    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    balance = Column(Integer)

    items = relationship("Item", back_populates="owner")


class Item(Base):
    "Item class of creating db table"

    __tablename__ = "items"

    id = Column(Integer, primary_key=True, index=True)
    gender = Column(String, index=True)
    age_at_diagnosis = Column(Float)
    race = Column(String, index=True)
    idh1 = Column(String, index=True)
    tp53 = Column(String, index=True)
    atrx = Column(String, index=True)
    pten = Column(String, index=True)
    egfr = Column(String, index=True)
    cic = Column(String, index=True)
    muc16 = Column(String, index=True)
    pik3ca = Column(String, index=True)
    nf1 = Column(String, index=True)
    pik3r1 = Column(String, index=True)
    fubp1 = Column(String, index=True)
    rb1 = Column(String, index=True)
    notch1 = Column(String, index=True)
    bcor = Column(String, index=True)
    csmd3 = Column(String, index=True)
    smarca4 = Column(String, index=True)
    grin2a = Column(String, index=True)
    idh2 = Column(String, index=True)
    fat4 = Column(String, index=True)
    pdgfra = Column(String, index=True)
    owner_id = Column(Integer, ForeignKey("users.id"))

    owner = relationship("User", back_populates="items")
