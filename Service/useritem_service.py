from select import select
from typing import Optional, List

from sqlalchemy.orm import Session

from Database.database import get_db
from Database.models import UserItem
from .item_service import ItemService

"""
useritem crud
"""
class UserItemService:

    @staticmethod
    def init_userItem(user_id: str):
        item = ItemService.get_all()
        with get_db() as db:
            for i in item:
                useritem = UserItem(user_id=user_id, item_name=i.item_name, count=0, consume_expectation=i.base_consume_expectation)
                db.add(useritem)
            db.commit()
        return True
    
    def get_all_userItem(user_id: str):
        with get_db() as db:
            return db.query(UserItem).filter(UserItem.user_id == user_id).all()
        
    def to_userItem_dict(userItemList: List[UserItem]):
        return [{
            "user_id": userItem.user_id,
            "item_name": userItem.item_name,
            "count": userItem.count,
            "consume_date": userItem.consume_date,
            "consume_expectation": userItem.consume_expectation
        } for userItem in userItemList]