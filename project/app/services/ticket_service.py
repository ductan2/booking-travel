from typing import Optional

from fastapi import HTTPException, UploadFile
from sqlalchemy import select
from sqlalchemy.exc import InvalidRequestError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload , selectinload
from app.models import TicketTravel, Location, Category, User
from app.schemas.ticket_schema import TicketCreate, TicketUpdate
from app.utils.cloudinary import upload_image


async def get_ticket_by_id(ticket_id: int, db: AsyncSession):
    result = await db.execute(select(TicketTravel).filter(TicketTravel.id == ticket_id))
    ticket = result.scalars().first()
    if not ticket:
        raise HTTPException(status_code=404, detail="Ticket not found")
    return ticket


async def get_all_tickets(
        db: AsyncSession,
        name: str = None,
        location_name: str = None,
        category_name: str = None
):
    query = select(TicketTravel).options(
        joinedload(TicketTravel.location),
        joinedload(TicketTravel.category),
        joinedload(TicketTravel.user)
    )

    if name:
        query = query.filter(TicketTravel.title.ilike(f"%{name}%"))
    if location_name:
        query = query.join(TicketTravel.location).filter(Location.name.ilike(f"%{location_name}%"))
    if category_name:
        query = query.join(TicketTravel.category).filter(Category.name.ilike(f"%{category_name}%"))

    result = await db.execute(query)
    return result.unique().scalars().all()


def ticket_to_dict(ticket: TicketTravel):
    ticket_dict = {
        "id": ticket.id,
        "title": ticket.title,
        "address": ticket.address,
        "location": ticket.location.name if ticket.location else None,
        "bed": ticket.bed,
        "people": ticket.people,
        "dateTour": ticket.dateTour,
        "description": ticket.description,
        "distance": ticket.distance,
        "duration": ticket.duration,
        "price": ticket.price,
        "score": ticket.score,
        "timeTour": ticket.timeTour,
        "tourGuideName": ticket.tourGuideName,
        "tourGuidePhone": ticket.tourGuidePhone,
        "tourGuidePic": ticket.tourGuidePic,
        "user": ticket.user.email if ticket.user else None,
        "category_name": ticket.category.name if ticket.category else None
    }
    return ticket_dict


async def get_bookmarked_tickets(user_id: int, db: AsyncSession):
    result = await db.execute(select(User).options(selectinload(User.bookmarked_items)).filter(User.id == user_id))
    user = result.scalars().first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user.bookmarked_items


async def create_ticket(data: TicketCreate, db: AsyncSession):
    new_ticket = TicketTravel(**data.dict())
    db.add(new_ticket)
    try:
        await db.commit()
        await db.refresh(new_ticket)
    except InvalidRequestError as e:
        await db.rollback()
        raise HTTPException(status_code=400, detail="Failed to create ticket") from e
    return new_ticket


async def update_ticket(ticket_id: int, ticket: TicketUpdate, db: AsyncSession):
    db_ticket = await get_ticket_by_id(ticket_id, db)
    ticket_data = ticket.dict(exclude_unset=True)
    for key, value in ticket_data.items():
        setattr(db_ticket, key, value)
    await db.commit()
    await db.refresh(db_ticket)
    return db_ticket


async def update_ticket_image(ticket_id: int, image: UploadFile, db: AsyncSession):
    db_ticket = await get_ticket_by_id(ticket_id, db)
    image_url = await upload_image(image)
    db_ticket.tourGuidePic = image_url
    await db.commit()
    await db.refresh(db_ticket)
    return db_ticket


async def delete_ticket(ticket_id: int, db: AsyncSession):
    db_ticket = await get_ticket_by_id(ticket_id, db)
    await db.delete(db_ticket)
    await db.commit()
    return db_ticket
