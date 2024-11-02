from select import select
from typing import Optional, List

from sqlalchemy.orm import Session

from Database.models import Item


class ItemService:
    @staticmethod
    def get_all(db_session: Session):
        return db_session.query(Item).all()