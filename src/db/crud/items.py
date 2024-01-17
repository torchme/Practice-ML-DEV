from sqlalchemy.orm import Session
from src.db.core import Item


def create_item(db: Session, item_data: dict):
    db_item = Item(**item_data)
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item
