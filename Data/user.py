from pydantic import BaseModel

class User(BaseModel):
    user_id : int
    name : str
    password : str

class UserRead(User):
    pass

class UserCreate(User):
    pass