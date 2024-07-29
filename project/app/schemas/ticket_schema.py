from fastapi import UploadFile
from pydantic import BaseModel, confloat, Field, conint
from typing import Optional
from datetime import datetime


class TicketCreate(BaseModel):
    title: str = Field(..., min_length=1, max_length=100)
    address: str = Field(...)
    bed: conint(ge=1, le=20) = Field(...)
    people: conint(ge=1, le=40) = Field(...)
    dateTour: str = Field(...)
    description: str = Field(...)
    distance: str = Field(..., max_length=150)
    duration: str = Field(...)
    price: confloat(gt=0) = Field(...)
    score: confloat(ge=0, le=5) = Field(...)
    timeTour: str = Field(...)
    tourGuideName: str = Field(..., max_length=100)
    tourGuidePhone: str = Field(..., max_length=15)
    tourGuidePic: str = Field(..., max_length=2083)
    category_id: int = Field(...)
    user_id: int = Field(...)
    location_id: int = Field(...)

    class Config:
        orm_mode = True


class TicketCreateForm(BaseModel):
    ticket_data: TicketCreate
    image: Optional[UploadFile] = None

    class Config:
        orm_mode = True
        arbitrary_types_allowed = True


class TicketUpdate(BaseModel):
    #Optional fields
    title: Optional[str] = None
    address: Optional[str] = None
    bed: Optional[int] = None
    people: Optional[int] = None
    dateTour: Optional[str] = None
    description: Optional[str] = None
    distance: Optional[str] = None
    duration: Optional[str] = None
    price: Optional[float] = None
    score: Optional[float] = None
    timeTour: Optional[str] = None
    tourGuideName: Optional[str] = None
    tourGuidePhone: Optional[str] = None
    tourGuidePic: Optional[str] = None
    category_id: Optional[int] = None
    user_id: Optional[int] = None
    location_id: Optional[int] = None


class TicketTravel(BaseModel):
    id: int
    title: str
    address: str
    bed: int
    people: int
    dateTour: datetime
    description: str
    distance: str
    duration: str
    price: float
    score: float
    timeTour: datetime
    tourGuideName: str
    tourGuidePhone: str
    tourGuidePic: str
    category_id: int
    user_id: int
    location_id: int

    class Config:
        orm_mode = True
