from typing import List

from fastapi.responses import JSONResponse

from Data.user import LoginUser, UserCreate
from Database.database import get_db
from fastapi import APIRouter
from starlette.status import *
from fastapi import Query, Request
from Data.item import Item, ItemAdd
from Database.models import User
from Service.purchase_service import PurchaseService
from Service.useritem_service import UserItemService
router = APIRouter(tags=["items"], prefix="/items")

@router.post("/add")
def add_item(request: Request, itemadd: ItemAdd):
    purchase_history_list = PurchaseService.purchase_history_list_db(itemadd.items)
    PurchaseService.purchase_history_list_save(purchase_history_list)
    return JSONResponse(status_code=HTTP_200_OK, content={"message": "Item added successfully"})


"""
유저가 보유한 모든 아이템을 가져온다.
"""
@router.get("/{user_id}/item", response_model=List[Item])
def get_userItem_all(request : Request, user_id: str):
    user_item_list = UserItemService.get_all_userItem(user_id)
    user_item_list_dict = UserItemService.to_userItem_dict(user_item_list)
    return JSONResponse(status_code=HTTP_200_OK, content={"items": user_item_list_dict})


"""
유저가 아이템 소비
TODO : request body에 아이템 개수 추가
"""
@router.post("/{user_id}/item/{item_id}/consume")
def consume_item(request : Request, user_id: str, item_id: str):
    return JSONResponse(status_code=HTTP_200_OK, content={"message": "Item consumed successfully"})


"""
유저가 아이템 추가
TODO : request body에 아이탬 개수 추가
"""
@router.post("/{user_id}/item/{item_id}/addition")
def add_item(request : Request, user_id: str, item_id: str):
    return JSONResponse(status_code=HTTP_200_OK, content={"message": "Item added successfully"})


"""
유저가 영수증 / 직접 아이템 추가
"""
@router.post("/{user_id}/receipt")
def add_items(request : Request, user_id: str):
    return JSONResponse(status_code=HTTP_200_OK, content={"message": "Item added successfully"})


@router.post("/signup")
def signup(request: Request, userCreate: UserCreate):
    user = User(
        name=userCreate.name,
        password=userCreate.password
    )
    with get_db() as db:
        db.add(user)
        db.commit()
        db.refresh(user)

    UserItemService.init_userItem(user.user_id)
    return JSONResponse(status_code=HTTP_200_OK, content={"message": "User added successfully"})


@router.post("/signin")
def signin(request: Request, user: LoginUser):
    with get_db() as db:
        user = db.query(User).filter(User.name == user.name).first()
        if user is None:
            return JSONResponse(status_code=HTTP_204_NO_CONTENT, content={"message": "User not found"})

        return JSONResponse(status_code=HTTP_200_OK, content={"message": "User signed in successfully", "user_id": user.user_id})