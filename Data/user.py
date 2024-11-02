from pydantic import BaseModel

class User(BaseModel):
    id : int
    name : str
    email : str
    password : str

class UserRead(User):
    pass

class UserCreate(User):
    pass