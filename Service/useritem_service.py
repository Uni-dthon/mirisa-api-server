from select import select
from typing import Optional, List

from sqlalchemy.orm import Session

from Database.models import UserItem
from .item_service import ItemService

"""
useritem crud
"""
class UserItemService:

    @staticmethod
    def init_userItem(db_session : Session, user_id: str):
        item = ItemService.get_all(db_session)
        for i in item:
            useritem = UserItem(user_id=user_id, item_name=i.item_name, count=0, consume_expectation=i.base_consume_expectation)
            db_session.add(useritem)
        db_session.commit()
        return True