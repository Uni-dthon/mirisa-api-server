from datetime import timedelta, datetime
from select import select
from typing import Optional, List, Annotated

from sqlalchemy.sql.expression import extract

from Data.item import UserItemAdd, ItemAdd, UserItemConsume
from Database.database import get_db
from Database.models import UserItem, Item
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
            return db.query(UserItem).filter(UserItem.user_id == user_id, UserItem.count > 0).all()

    def get_all_userItem_filtered_by_category(user_id: str, category: str):
        with get_db() as db:
            return db.query(UserItem).filter(UserItem.user_id == user_id, UserItem.count > 0).join(Item).filter(Item.item_category == category).all()

    def get_all_userItem_filtered_by_date(user_id, year: int, month: int):
        with get_db() as db:
            return db.query(UserItem).filter(UserItem.user_id == user_id, extract("year", UserItem.consume_date) == year,
                    extract("month", UserItem.consume_date) == month).all()


    def to_userItem_dict_with_category(userItemList: List[UserItem], category: str):
        itemlist = []

        for userItem in userItemList:
            itemlist.append({
                "user_id": userItem.user_id,
                "item_name": userItem.item_name,
                "count": userItem.count,
                "category": category,
                "consume_date": userItem.consume_date.strftime("%Y-%m-%d") if userItem.consume_date is not None else None,
            })
        return itemlist

    @staticmethod
    def to_userItem_dict(userItemList: List[UserItem]):
        itemlist = []

        with get_db() as db:
            for userItem in userItemList:
                item = db.query(Item).filter(Item.item_name == userItem.item_name).first()
                itemlist.append({
                    "user_id": userItem.user_id,
                    "item_name": userItem.item_name,
                    "count": userItem.count,
                    "category": item.item_category,
                    "consume_date": userItem.consume_date.strftime("%Y-%m-%d") if userItem.consume_date is not None else None,
                })
        return itemlist

    def add_userItem(itemAdd: UserItemAdd):
        with get_db() as db:
            useritem = db.query(UserItem).filter(UserItem.user_id == itemAdd.user_id, UserItem.item_name == itemAdd.item_name).first()
            if useritem is None:
                raise Exception("UserItem not found")

            if useritem.consume_date is None or useritem.count == 0:
                useritem.consume_date = itemAdd.purchase_date

            useritem.count += itemAdd.count
            useritem.consume_date += timedelta(days=useritem.consume_expectation * itemAdd.count)
            db.commit()
        return True


    @staticmethod
    def add_userItems(itemAdd : ItemAdd):
        with get_db() as db:
            for addItem in itemAdd.items:
                useritem = db.query(UserItem).filter(UserItem.user_id == addItem.user_id, UserItem.item_name == addItem.item_name).first()

                if useritem.consume_date is None or useritem.count == 0:
                    useritem.consume_date = addItem.purchase_date

                useritem.count += addItem.count
                useritem.consume_date += timedelta(days=useritem.consume_expectation * addItem.count)
            db.commit()
        return True
    
    def consume_userItem(userItemConsume: UserItemConsume):
        with get_db() as db:
            useritem = db.query(UserItem).filter(UserItem.user_id == userItemConsume.user_id, UserItem.item_name == userItemConsume.item_name).first()
            if useritem.count - userItemConsume.consume_count < 0:
                return False
            useritem.count -= userItemConsume.consume_count
            db.commit()
        return True