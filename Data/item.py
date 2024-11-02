from pydantic  import BaseModel
from datetime import date

class Item(BaseModel):
    user_id : int
    item_name : str


class ItemRead(Item):
    count : int
    category : str
    consume_date: date

class ItemConsume(Item):
    consume_count: int

class UserItemAdd(BaseModel):
    user_id: str
    item_name: str
    count: int
    price: int
    purchase_date: date

class ItemAdd(Item):
    items: list[UserItemAdd]