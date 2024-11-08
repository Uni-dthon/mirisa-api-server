from typing import List
from Data.item import *
from Database.models import *

class PurchaseService:
    def purchase_history_list_db(item: ItemAdd):
        data_list = []
        with get_db() as db:
            for item_add in item.items:
                item_id = db.query(UserItem).filter(UserItem.user_id == item_add.user_id, UserItem.item_name == item_add.item_name).first().item_id
                if item_add.count > item_add.price:
                    data_list.append(PurchaseHistory(user_id=item_add.user_id, item_id=item_id, price=item_add.count, count=item_add.price, date=item_add.purchase_date))
                else:
                    data_list.append(PurchaseHistory(user_id=item_add.user_id, item_id=item_id, price=item_add.price, count=item_add.count, date=item_add.purchase_date))
        return data_list


    def purchase_history_list_save(data_list: List[PurchaseHistory]):
        with get_db() as db:
            db.add_all(data_list)
            db.commit()
            return True

    def purchase_history_db(data : UserItemAdd):
        with get_db() as db:
            item_id = db.query(UserItem).filter(UserItem.user_id == data.user_id, UserItem.item_name == data.item_name).first().item_id
            return PurchaseHistory(user_id=data.user_id, item_id=item_id, price=data.price, count=data.count, date=data.purchase_date)
        
    def purchase_history_save(data : PurchaseHistory):
        with get_db() as db:
            db.add(data)
            db.commit()


    def get_purchase_histories_by_item_id(item_id: str):
        with get_db() as db:
            return db.query(PurchaseHistory).filter(PurchaseHistory.item_id == item_id).all()