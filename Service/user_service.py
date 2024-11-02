from Database.database import get_db
from Database.models import User
from Service.useritem_service import UserItemService


class UserService:
    @staticmethod
    def get_user_by_id(user_id: str):
        with get_db() as db:
            return db.query(User).filter(User.user_id == user_id).first()

    @staticmethod
    def get_user_or_create(user_id: str, name=None, password="1234"):
        user = UserService.get_user_by_id(user_id)
        if user is None:
            with get_db() as db:
                user = User(name=user_id[:8] if name is None else name, password=password)
                db.add(user)
                db.commit()
                db.refresh(user)
            UserItemService.init_userItem(user.user_id)
        return user