from fastapi.responses import JSONResponse
from Database.database import get_db
from fastapi import APIRouter
from starlette.status import *
from fastapi import Query, Request
from Data.item import Item, ItemAdd
from Database.models import User
from Service.purchase_service import PurchaseService
router = APIRouter(tags=["items"], prefix="/items")

@router.post("/add")
def add_item(request: Request, itemadd: ItemAdd):
    purchase_history_list = PurchaseService.purchase_history_list_db(itemadd.items)
    PurchaseService.purchase_history_list_save(purchase_history_list)
    return JSONResponse(status_code=HTTP_200_OK, content={"message": "Item added successfully"})

@router.get("/test")
def test():
    from Database.models import hash_id
    print(hash_id())
    return JSONResponse(status_code=HTTP_200_OK, content={"message": "User added successfully"})