from pydantic import BaseModel

class UserCreate(BaseModel):
    username: str
    email: str
    password: str

class UserInDB(UserCreate):
    id: int

    class Config:
        orm_mode = True

class UserOut(BaseModel):
    id: int
    username: str
    email: str

    class Config:
        from_attributes = True  
