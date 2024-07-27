from sqlmodel import SQLModel, Field
from typing import Optional


class BaseModel(SQLModel):
    id: Optional[int] = Field(default=None, primary_key=True)

    class Config:
        from_attributes = True


class User(BaseModel, table=True):
    username: str = Field(unique=True, index=True)
    email: str = Field(unique=True, index=True)
    password: str = Field(min_length=8, max_length=128)
    address: Optional[str] = None
    phone: Optional[str] = None


class Category(BaseModel, table=True):
    name: str = Field(unique=True, index=True)
    description: Optional[str] = None
