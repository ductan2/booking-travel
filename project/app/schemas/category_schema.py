from typing import Optional

from pydantic import BaseModel


class CategoryBase(BaseModel):
    id: int
    name: str
    description: Optional[str]

    class Config:
        orm_mode = True


class CategoryCreate(BaseModel):
    name: str
    description: Optional[str]

    class Config:
        orm_mode = True


class CategoryUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None

    class Config:
        orm_mode = True
