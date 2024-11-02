from typing import List

from fastapi.responses import JSONResponse

from Data.user import LoginUser, UserCreate
from Database.database import get_db
from fastapi import APIRouter
from starlette.status import *
from fastapi import Query, Request
from Data.item import Item, ItemAdd, UserItemAdd, UserItemConsume, ItemRead
from Database.models import User
from Service.item_service import ItemService
from Service.purchase_service import PurchaseService
from Service.useritem_service import UserItemService
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
@router.post("/{user_id}/item/{item_name}/consume")
def consume_item(request : Request, user_id: str, user_item_consume: UserItemConsume):
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
    UserItemService.add_userItem(userItemAdd)
    purchaseHistory = PurchaseService.purchase_history_db(userItemAdd)
    PurchaseService.purchase_history_save(purchaseHistory)
    return JSONResponse(status_code=HTTP_200_OK, content={"message": "Item added successfully"})


@router.get("/{user_id}/price")
def get_expected_price(request : Request, user_id: str, date : str = Query(...)):
    try:
        year, month = map(int, date.split("-"))

        user_item_list = UserItemService.get_all_userItem_filtered_by_date(user_id, year, month)

        price = 0
        for useritem in user_item_list:
            purchases = PurchaseService.get_purchase_histories_by_item_id(useritem.item_id)
            if len(purchases) == 0:
                item = ItemService.get_item(useritem.item_name)
                price += item.base_price * item.base_count
            else:
                avg_count = round(sum([purchase.count for purchase in purchases]) / len(purchases))
                avg_price = sum([purchase.price for purchase in purchases]) / len(purchases)
                price += avg_count * avg_price

        return JSONResponse(status_code=HTTP_200_OK, content={"price": price})

    except ValueError:
        return JSONResponse(status_code=HTTP_400_BAD_REQUEST, content={"message": "Invalid date format"})
    except Exception as e:
        return JSONResponse(status_code=HTTP_500_INTERNAL_SERVER_ERROR, content={"message": str(e)})