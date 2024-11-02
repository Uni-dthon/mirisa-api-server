from typing import List

from fastapi.responses import JSONResponse

from Data.user import LoginUser, UserCreate
from Database.database import get_db
from fastapi import APIRouter
from starlette.status import *
from fastapi import Query, Request
from Data.item import Item, ItemAdd, UserItemAdd, UserItemConsume, ItemRead
from Database.models import ItemCategory
from Service.embedding_service import EmbeddingService
from Service.item_service import ItemService
from Service.purchase_service import PurchaseService
from Service.useritem_service import UserItemService
import numpy as np
router = APIRouter(tags=["items"], prefix="/items")
"""
물품을 리스트로 추가한다.
"""
@router.post("/addall")
def add_items(request: Request, itemadd: ItemAdd):
    UserItemService.add_userItems(itemadd)
    purchase_history_list = PurchaseService.purchase_history_list_db(itemadd)
    PurchaseService.purchase_history_list_save(purchase_history_list)
    return JSONResponse(status_code=HTTP_200_OK, content={"message": "Item added successfully"})


"""
유저가 보유한 모든 아이템을 가져온다.
"""
@router.get("/{user_id}/item", response_model=List[ItemRead])
def get_userItem_all(request : Request, user_id: str):
    user_item_list = UserItemService.get_all_userItem(user_id)
    user_item_list_dict = UserItemService.to_userItem_dict(user_item_list)
    return JSONResponse(status_code=HTTP_200_OK, content={"items": user_item_list_dict})


"""
유저가 아이템 소비
TODO : request body에 아이템 개수 추가
"""
@router.post("/consume")
def consume_item(request : Request, user_item_consume: UserItemConsume):
    result = UserItemService.consume_userItem(user_item_consume)
    if result is False:
        return JSONResponse(status_code=HTTP_400_BAD_REQUEST, content={"message": "Item consume failed"})
    return JSONResponse(status_code=HTTP_200_OK, content={"message": "Item consumed successfully"})


"""
유저가 아이템 추가
TODO : request body에 아이탬 개수 추가
"""
@router.post("/addone")
def add_item(request : Request, userItemAdd: UserItemAdd):
    try:
        UserItemService.add_userItem(userItemAdd)
        purchaseHistory = PurchaseService.purchase_history_db(userItemAdd)
        PurchaseService.purchase_history_save(purchaseHistory)
        return JSONResponse(status_code=HTTP_200_OK, content={"message": "Item added successfully"})
    except OverflowError as e:
        return JSONResponse(status_code=HTTP_400_BAD_REQUEST, content={"message": "Too many items added"})
    

@router.get("/add/{item_name}/{base_consume_expectation}/{base_price}")
def add_item(request : Request, item_name: str, base_consume_expectation: int, base_price: int):
    category_embedding = []
    for category in ItemCategory.list():
        print(category)
        if (temp := EmbeddingService.embedding(category)) is False:
            return JSONResponse(status_code=HTTP_400_BAD_REQUEST, content={"message": "Item added failed"})
        category_embedding.append(temp)
    item_embedding = EmbeddingService.embedding(item_name)
    for i in range(len(category_embedding)):
        category_embedding[i] = cosine_similarity(category_embedding[i], item_embedding)
    ItemCategory.list()[find_max_index(category_embedding)]
    return JSONResponse(status_code=HTTP_200_OK, content={"message": "Item added successfully"})

def cosine_similarity(vec1, vec2):
    dot_product = np.dot(vec1, vec2)
    norm_vec1 = np.linalg.norm(vec1)
    norm_vec2 = np.linalg.norm(vec2)
    return dot_product / (norm_vec1 * norm_vec2)

def find_max_index(lst):
    if not lst:
        return None  # 리스트가 비어있으면 None 반환
    max_value = max(lst)
    max_index = lst.index(max_value)
    return max_index