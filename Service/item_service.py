from select import select
from typing import Optional, List

from sqlalchemy.orm import Session

from Database.database import get_db
from Database.models import Item


class ItemService:
    @staticmethod
    def get_all():
        with get_db() as db:
            return db.query(Item).all()