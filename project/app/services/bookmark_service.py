from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload, selectinload, selectin_polymorphic

from app.models import UserBookmarked, User, TicketTravel


async def get_bookmark_tickets(user_id: int, db: AsyncSession):
    bookmark_query = select(UserBookmarked.ticket_travel_id).filter(UserBookmarked.user_id == user_id)
    result = await db.execute(bookmark_query)
    ticket_ids = result.scalars().all()

    if ticket_ids:
        tickets_query = (
            select(TicketTravel)
            .options(
                joinedload(TicketTravel.category),
                joinedload(TicketTravel.location),
                joinedload(TicketTravel.user)
            )
            .filter(TicketTravel.id.in_(ticket_ids))
        )
        tickets_result = await db.execute(tickets_query)
        tickets = tickets_result.unique().scalars().all()

        ticket_dicts = [ticket_to_dict(ticket) for ticket in tickets]
        return ticket_dicts
    else:
        return []


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


async def addBookmark(user_id: int, ticket_id: int, db: AsyncSession):
    print(user_id, ticket_id)
    # Check if user exists
    user_query = select(User).where(User.id == user_id)
    user = await db.execute(user_query)
    user = user.scalar_one_or_none()
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")

    ticket_query = select(TicketTravel).where(TicketTravel.id == ticket_id)
    ticket = await db.execute(ticket_query)
    ticket = ticket.scalar_one_or_none()
    if ticket is None:
        raise HTTPException(status_code=404, detail="Ticket not found")

    bookmark_query = select(UserBookmarked).where(
        (UserBookmarked.user_id == user_id) & (UserBookmarked.ticket_travel_id == ticket_id)
    )
    existing_bookmark = await db.execute(bookmark_query)
    existing_bookmark = existing_bookmark.scalar_one_or_none()

    if existing_bookmark is not None:
        await db.delete(existing_bookmark)
        await db.commit()
        return None
    else:
        bookmark = UserBookmarked(user_id=user_id, ticket_travel_id=ticket_id)
        db.add(bookmark)
        await db.commit()
        await db.refresh(bookmark)
        return bookmark
