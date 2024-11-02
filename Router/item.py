from typing import List

from fastapi.responses import JSONResponse
from Database.database import get_db
from fastapi import APIRouter
from starlette.status import *
from fastapi import Query, Request
from Data.item import Item
from Database.models import User
router = APIRouter(tags=["items"], prefix="/items")

@router.post("/add")
def add_item(request: Request, item: Item):
    return JSONResponse(status_code=HTTP_200_OK, content={"message": "Item added successfully"})


"""
유저가 보유한 모든 아이템을 가져온다.
"""
@router.get("/{user_id}/item", response_model=List[Item])
def get_userItem_all(request : Request, user_id: str):
    return JSONResponse(status_code=HTTP_200_OK, content={"message": "Item added successfully"})


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



@router.get("/test")
def test():
    with get_db() as db:
        newuser = User(name="test", password="test")
        db.add(newuser)
        db.commit()
    return JSONResponse(status_code=HTTP_200_OK, content={"message": "User added successfully"})