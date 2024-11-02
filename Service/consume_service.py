from typing import List
from Data.item import *
from Database.models import *

class ConsumeService:
    def consume_history_db(data : UserItemConsume):
        with get_db() as db:
            item_id = db.query(UserItem).filter(UserItem.user_id == data.user_id, UserItem.item_name == data.item_name).first().item_id
            return ConsumeHistory(user_id=data.user_id, item_id=item_id, count=data.consume_count, date=data.consume_date)
        
    def purchase_history_save(data : ConsumeHistory):
        with get_db() as db:
            db.add(data)
            db.commit()

    def get_consume_histories_by_item_id(item_id: str):
        with get_db() as db:
            return db.query(ConsumeHistory).filter(ConsumeHistory.item_id == item_id).order_by(ConsumeHistory.date.asc()).all()