from pydantic import BaseModel

class UserBase(BaseModel):
    name : str
    password : str

class UserRead(UserBase):
    user_id : str

class UserCreate(UserBase):
    pass

class LoginUser(UserBase):
    pass