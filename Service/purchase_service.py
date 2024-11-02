from typing import List
from Data.item import *
from Database.models import *
class PurchaseService:

    def purchase_history_list_db(item: ItemAdd):
        data_list = []
        with get_db() as db:
            for item_add in item.items:
                item_id = db.Query(UserItem).filter(UserItem.user_id == item_add.user_id, UserItem.item_name == item_add.item_name).first().item_id
                data_list.append(PurchaseHistory(user_id=item_add.user_id, item_id=item_id, price=item_add.price, date=item_add.purchase_date))
        
    def purchase_history_list_save(data_list: List[PurchaseHistory]):
        with get_db() as db:
            db.add_all(data_list)
            db.commit()
            return True
        
    