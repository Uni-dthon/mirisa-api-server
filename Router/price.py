from fastapi.responses import JSONResponse

from Data.user import LoginUser, UserCreate
from Database.database import get_db
from fastapi import APIRouter
from starlette.status import *
from fastapi import Query, Request
from Database.models import User
from Service.item_service import ItemService
from Service.purchase_service import PurchaseService
from Service.useritem_service import UserItemService


router = APIRouter(tags=["price"], prefix="/price")

@router.get("/{user_id}")
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