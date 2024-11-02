from pydantic  import BaseModel
from datetime import date

class Item(BaseModel):
    user_id : int
    item_name : str
    count : int

class ItemRead(Item):
    consume_date : date

class ItemCreate(Item):
    pass


class ItemUpdate(Item):
    consume_date: date
    