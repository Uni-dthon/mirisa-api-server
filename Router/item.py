from fastapi.responses import JSONResponse
from Database.database import get_db
from fastapi import APIRouter
from starlette.status import *
from fastapi import Query, Request
from item import Item

router = APIRouter(tags=["items"], prefix="/items")

@router.post("/add")
def add_item(request: Request, item: Item):
    return JSONResponse(status_code=HTTP_200_OK, content={"message": "Item added successfully"})