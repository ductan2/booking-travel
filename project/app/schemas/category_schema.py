from typing import Optional

from fastapi import UploadFile
from pydantic import BaseModel


class CategoryBase(BaseModel):
    id: int
    name: str
    description: Optional[str]
    image: Optional[str]

    class Config:
        orm_mode = True


class CategoryCreate(BaseModel):
    name: str
    description: Optional[str]
    image: Optional[UploadFile] = None

    class Config:
        orm_mode = True


class CategoryUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    image: Optional[UploadFile] = None

    class Config:
        orm_mode = True
