from pydantic import BaseModel
from typing import Optional


class LocationBase(BaseModel):
    name: str
    description: Optional[str] = None


class LocationCreate(LocationBase):
    pass


class LocationUpdate(LocationBase):
    pass


class Location(LocationBase):
    id: int

    class Config:
        orm_mode = True
