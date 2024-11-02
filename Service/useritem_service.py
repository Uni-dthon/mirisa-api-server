from datetime import timedelta, datetime
from select import select
from typing import Optional, List, Annotated

from sqlalchemy.orm import Session

from Data.item import UserItemAdd, ItemAdd
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

    def add_userItem(itemAdd: UserItemAdd):
        with get_db() as db:
            useritem = db.query(UserItem).filter(UserItem.user_id == itemAdd.user_id, UserItem.item_name == itemAdd.item_name).first()

            if useritem.consume_date is None or useritem.count == 0:
                useritem.consume_date = itemAdd.purchase_date

            useritem.count += itemAdd.count
            useritem.consume_date += timedelta(days=useritem.consume_expectation * itemAdd.count)
            db.commit()
        return True

    @staticmethod
    def add_userItems(itemAdd : ItemAdd):
        for addItem in itemAdd.items:
            with get_db() as db:
                useritem = db.query(UserItem).filter(UserItem.user_id == addItem.user_id, UserItem.item_name == addItem.item_name).first()

                if useritem.consume_date is None or useritem.count == 0:
                    useritem.consume_date = addItem.purchase_date

                useritem.count += addItem.count
                useritem.consume_date += timedelta(days=useritem.consume_expectation * addItem.count)
                db.commit()
        return True