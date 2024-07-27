from sqlmodel import SQLModel, Field, Relationship
from typing import Optional, List


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

    tickets: List["TicketTravel"] = Relationship(back_populates="user")
    bookmarked_items: List["UserBookmarked"] = Relationship(back_populates="user")


class Category(BaseModel, table=True):
    name: str = Field(unique=True, index=True)
    description: Optional[str] = None
    image: str = Field(max_length=2083, nullable=True)

    tickets: List["TicketTravel"] = Relationship(back_populates="category")


class Location(BaseModel, table=True):
    name: str = Field(unique=True, index=True)
    description: Optional[str] = None

    tickets: List["TicketTravel"] = Relationship(back_populates="location")


class TicketTravel(BaseModel, table=True):
    title: str = Field(min_length=1, max_length=100)
    address: str = Field()
    bed: int = Field(ge=1, le=20)
    people: int = Field(ge=1, le=40)
    dateTour: str = Field()
    description: str = Field()
    distance: str = Field(max_length=150)
    duration: str = Field()
    price: float = Field(gt=0)
    score: float = Field(ge=0, le=5)
    timeTour: str
    tourGuideName: str = Field(max_length=100)
    tourGuidePhone: str = Field(max_length=15)
    tourGuidePic: str = Field(max_length=2083)
    category_id: int = Field(foreign_key="category.id", index=True)
    user_id: int = Field(foreign_key="user.id", index=True)
    location_id: int = Field(foreign_key="location.id", index=True)
    image: str = Field(max_length=2083, nullable=True)

    category: Category = Relationship(back_populates="tickets")
    user: User = Relationship(back_populates="tickets")
    location: Location = Relationship(back_populates="tickets")
    ticket_bookmarked: List["UserBookmarked"] = Relationship(back_populates="ticket_travel")


class UserBookmarked(BaseModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: int = Field(foreign_key="user.id", index=True)
    ticket_travel_id: int = Field(foreign_key="tickettravel.id", index=True)

    ticket_travel: TicketTravel = Relationship(back_populates="ticket_bookmarked")
    user: User = Relationship(back_populates="bookmarked_items")


# Resolve forward references after all models are defined
SQLModel.update_forward_refs()
