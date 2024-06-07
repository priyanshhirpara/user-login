from pydantic import BaseModel, EmailStr
from enum import Enum
from datetime import date
from typing import Optional

# from typing import Optional


class UserType(Enum):
    ADMIN = "admin"
    STUDENT = "student"
    TEACHER = "teacher"


class User(BaseModel):
    firstname: str
    lastname: str
    username: str
    email: str
    password: str
    birthdate: date
    user_type: UserType


class Login(BaseModel):
    email: str
    password: str


class ShowUser(BaseModel):
    email: EmailStr
    birthdate: str
    username: str


class TokenData(BaseModel):
    email: Optional[str] = None


class UserInDB(User):
    hashed_password: str
