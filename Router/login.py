from fastapi.responses import JSONResponse

from Data.user import LoginUser, UserCreate
from Database.database import get_db
from fastapi import APIRouter
from starlette.status import *
from fastapi import Query, Request
from Database.models import User
from Service.useritem_service import UserItemService
from Utils.swagger import signin_response_example

router = APIRouter(tags=["login"], prefix="/login")


@router.post("/signup", summary="회원가입", description="회원가입", responses={
    200: {"description": "성공", "content": {"application/json": {"example": {"message": "User added successfully"}}}},
    500: {"description": "실패"}
})
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


@router.post("/signin", summary="로그인", description="로그인 패스워드 확인안함", responses={
    200: {"description": "성공", "content": {"application/json": {"example": signin_response_example}}},
    204: {"description": "유저 없음", "content": {"application/json": {"example": {"message": "User not found"}}}},
    500: {"description": "실패"}
})
def signin(request: Request, user: LoginUser):
    with get_db() as db:
        user = db.query(User).filter(User.name == user.name).first()
        if user is None:
            return JSONResponse(status_code=HTTP_204_NO_CONTENT, content={"message": "User not found"})

        return JSONResponse(status_code=HTTP_200_OK, content={"message": "User signed in successfully", "user_id": user.user_id})