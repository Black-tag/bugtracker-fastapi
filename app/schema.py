from pydantic import BaseModel

class Bug(BaseModel):
    title: str 
    description: str 


    class config:
        orm_mod = True

class User(BaseModel):
    name: str


    class config:
        orm_mod = True 

class BugCreate(Bug):
    pass 

class UserCreate(User):
    pass

class UserUpdate(User):
    pass


class BugUpdate(Bug):
    pass
