from typing import List

from fastapi.responses import JSONResponse

from Data.user import LoginUser, UserCreate
from Database.database import get_db
from fastapi import APIRouter
from starlette.status import *
from fastapi import Query, Request
from Data.item import Item, ItemAdd, UserItemAdd
from Database.models import User
from Service.purchase_service import PurchaseService
from Service.useritem_service import UserItemService
router = APIRouter(tags=["items"], prefix="/items")

@router.post("/addall")
def add_items(request: Request, itemadd: ItemAdd):
    UserItemService.add_userItems(itemadd)
    purchase_history_list = PurchaseService.purchase_history_list_db(itemadd)
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
@router.post("/{user_id}/item/{item_name}/consume")
def consume_item(request : Request, user_id: str, item_name: str):
    return JSONResponse(status_code=HTTP_200_OK, content={"message": "Item consumed successfully"})


"""
유저가 아이템 추가
TODO : request body에 아이탬 개수 추가
"""
@router.post("/addone")
def add_item(request : Request, userItemAdd: UserItemAdd):
    UserItemService.add_userItem(userItemAdd)
    PurchaseService.purchase_history_save(userItemAdd)
    return JSONResponse(status_code=HTTP_200_OK, content={"message": "Item added successfully"})


"""
유저가 영수증 / 직접 아이템 추가
"""
@router.post("/{user_id}/receipt")
def add_items(request : Request, user_id: str):
    return JSONResponse(status_code=HTTP_200_OK, content={"message": "Item added successfully"})
