import random
import uuid
from sqlalchemy import JSON, DateTime, ForeignKey, Column, Index, Integer, PrimaryKeyConstraint, String, Time, Boolean, UniqueConstraint, event
from sqlalchemy.orm import relationship
from Database.database import Base, db, engine, get_db
from datetime import datetime, timezone, timedelta

class BaseEntity(Base):
    __abstract__ = True
    created_at = Column(DateTime, default=datetime.now(timezone.utc))
    updated_at = Column(DateTime, default=datetime.now(timezone.utc), onupdate=datetime.now(timezone.utc))
    is_deleted = Column(Boolean, default=False)

class User(BaseEntity):
    __tablename__ = "user"
    user_id = Column(Integer, primary_key=True, index=True)
    name = Column(String(50), nullable=False)
    password = Column(String(50), nullable=False)

class UserItem(BaseEntity):
    __tablename__ = "user_item"
    user_id = Column(Integer, nullable=False)
    item_name = Column(Integer, nullable=False)
    count = Column(Integer, nullable=False)
    consume_date = Column(DateTime, nullable=True)
    consume_expectation = Column(Integer, nullable=False)
    __table_args__ = (PrimaryKeyConstraint('user_id', 'item_id', name='user_item_pk'),)