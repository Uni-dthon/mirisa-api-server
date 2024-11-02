from statistics import mean
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

    def calculate_consume_expectation(user_id: str, item_name: str):
        with get_db() as db:
            item_id = db.query(UserItem).filter(UserItem.user_id == user_id, UserItem.item_name == item_name).first().item_id
            consume_histories = db.query(ConsumeHistory).filter(ConsumeHistory.item_id == item_id).order_by(ConsumeHistory.date).all()
        if len(consume_histories) < 2:
            return None
        date_differences = []
        for i in range(1, len(consume_histories)):
            date_diff = (consume_histories[i].date - consume_histories[i-1].date).days
            date_differences.append(date_diff)
        
        average_difference = round(mean(date_differences))
        if average_difference < 1:
            return 1
        return average_difference
    
    def set_consume_expectation(user_id: str, item_name: str, expectation: int):
        with get_db() as db:
            item_id = db.query(UserItem).filter(UserItem.user_id == user_id, UserItem.item_name == item_name).first().item_id
            user_item = db.query(UserItem).filter(UserItem.item_id == item_id).first()
            user_item.consume_expectation = expectation
            db.commit()



    def get_consume_histories_by_item_id(item_id: str):
        with get_db() as db:
            return db.query(ConsumeHistory).filter(ConsumeHistory.item_id == item_id).order_by(ConsumeHistory.date.asc()).all()