import enum
import random
import uuid
from sqlalchemy import JSON, DateTime, ForeignKey, Column, Index, Integer, PrimaryKeyConstraint, String, Time, Boolean, UniqueConstraint, event, Enum

from sqlalchemy.orm import relationship
from Database.database import Base, db, engine, get_db
from datetime import datetime, timezone, timedelta

def hash_id():
    return str(uuid.uuid4().hex)

class ItemCategory(str, enum.Enum):
    KITCHEN = "kitchen"
    BATHROOM = "bathroom"
    LIVINGROOM = "livingroom"
    CLEANROOM = "laundryroom"

    @classmethod
    def list(cls):
        return [category.value for category in cls]


class BaseEntity(Base):
    __abstract__ = True
    created_at = Column(DateTime, default=datetime.now(timezone.utc))
    updated_at = Column(DateTime, default=datetime.now(timezone.utc), onupdate=datetime.now(timezone.utc))
    is_deleted = Column(Boolean, default=False)


class User(BaseEntity):
    __tablename__ = "user"
    user_id = Column(String(50), default=hash_id, primary_key=True, index=True)
    name = Column(String(50), nullable=False)
    password = Column(String(50), nullable=False)


class Item(BaseEntity):
    __tablename__ = "item"
    id = Column(String(50), default=hash_id, primary_key=True, index=True)
    item_name = Column(String(50), index=True)
    item_category = Column(Enum(ItemCategory), nullable=False)
    base_consume_expectation = Column(Integer, nullable=False)
    base_price = Column(Integer, nullable=False)
    base_count = Column(Integer, nullable=False)
    embedding = Column(JSON, nullable=True)


class UserItem(BaseEntity):
    __tablename__ = "user_item"
    user_id = Column(String(50), ForeignKey("user.user_id"), nullable=False)
    item_id = Column(String(50), primary_key=True, default=hash_id, index=True)
    item_name = Column(String(50), ForeignKey("item.item_name"), nullable=False)
    count = Column(Integer, nullable=False)
    consume_date = Column(DateTime, nullable=True)
    consume_expectation = Column(Integer, nullable=False)

class ConsumeHistory(BaseEntity):
    __tablename__ = "consume_history"
    consume_history_id = Column(String(50), default=hash_id, primary_key=True, index=True)
    user_id = Column(String(50), nullable=False) #fk problems at here
    item_id = Column(String(50), nullable=False) #fk problems at here
    count = Column(Integer, nullable=False)
    date = Column(DateTime, nullable=False)

class PurchaseHistory(BaseEntity):
    __tablename__ = "purchase_history"
    purchase_history_id = Column(String(50), default=hash_id, primary_key=True, index=True)
    user_id = Column(String(50), nullable=False) #fk problems at here
    item_id = Column(String(50), nullable=False) #fk problems at here
    price = Column(Integer, nullable=False)
    count = Column(Integer, nullable=False)
    date = Column(DateTime, nullable=False)
