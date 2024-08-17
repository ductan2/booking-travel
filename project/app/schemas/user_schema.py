from typing import Optional

from pydantic import BaseModel, EmailStr


class UserBase(BaseModel):
    id: int
    email: EmailStr
    username: str
    password: str
    address: Optional[str]
    phone: Optional[str]

    class Config:
        orm_mode = True


class UserCreate(BaseModel):
    email: EmailStr
    username: str
    password: str

    class Config:
        orm_mode = True


class UserUpdatePass(BaseModel):
    old_password: str
    password: str


class UserLogin(BaseModel):
    account: str | EmailStr
    password: str

    class Config:
        orm_mode = True


class UserUpdate(BaseModel):
    # Optional fields
    email: Optional[EmailStr] = None
    username: Optional[str] = None
    password: Optional[str] = None
    address: Optional[str] = None
    phone: Optional[str] = None

    class Config:
        orm_mode = True


class UserPassword(BaseModel):
    old_password: str
    password: str

    class Config:
        orm_mode = True
