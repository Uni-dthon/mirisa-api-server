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


class ItemAdd(Item):
    add_count: int