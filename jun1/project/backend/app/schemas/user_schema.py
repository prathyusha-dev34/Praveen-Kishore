from pydantic import BaseModel, EmailStr

from pydantic import BaseModel

class UserPreferenceCreate(BaseModel):
    genre: str
    score: int

class UserRegister(BaseModel):
    name: str
    email: EmailStr
    password: str


class UserLogin(BaseModel):
    email: EmailStr
    password: str