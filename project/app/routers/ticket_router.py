import json
from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, Query, Form, UploadFile, File
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_session
from app.services import ticket_service, bookmark_service
from app.schemas.ticket_schema import TicketCreate, TicketUpdate, TicketTravel
from app.utils.cloudinary import upload_image

router = APIRouter()


@router.post("/")
async def create_ticket(
        ticket_data: str = Form(...),
        image: Optional[UploadFile] = File(None),
        db: AsyncSession = Depends(get_session)):
    ticket_dict = json.loads(ticket_data)
    print(ticket_dict)

    if image:
        image_url = await upload_image(image)
    else:
        image_url = None

    ticket = TicketCreate(
        tourGuidePic=image_url,
        **ticket_dict)
    return await ticket_service.create_ticket(ticket, db)


@router.get("/")
async def get_all_tickets(
        db: AsyncSession = Depends(get_session),
        name: Optional[str] = Query(None, description="Search by ticket title"),
        location: Optional[str] = Query(None, description="Search by location name"),
        category: Optional[str] = Query(None, description="Search by category name")
):
    tickets = await ticket_service.get_all_tickets(db, name, location, category)
    return [ticket_service.ticket_to_dict(ticket) for ticket in tickets]


@router.get("/{ticket_id}")
async def get_ticket_by_id(ticket_id: int, db: AsyncSession = Depends(get_session)):
    return await ticket_service.get_ticket_by_id(ticket_id, db)


@router.put("/{ticket_id}")
async def update_ticket(ticket_id: int, ticket: TicketUpdate, db: AsyncSession = Depends(get_session)):
    return await ticket_service.update_ticket(ticket_id, ticket, db)


@router.delete("/{ticket_id}")
async def delete_ticket(ticket_id: int, db: AsyncSession = Depends(get_session)):
    return await ticket_service.delete_ticket(ticket_id, db)


# @router.get("/bookmark/{user_id}")
# async def get_bookmarked_tickets(user_id: int, db: AsyncSession = Depends(get_session)):
#     return await ticket_service.get_bookmarked_tickets(user_id, db)


@router.patch("/image/{ticket_id}")
async def update_ticket_image(ticket_id: int, image: UploadFile = File(...), db: AsyncSession = Depends(get_session)):
    return await ticket_service.update_ticket_image(ticket_id,image , db)


@router.get("/bookmark/{user_id}")
async def bookmark_ticket(user_id: int, db: AsyncSession = Depends(get_session)):
    return await bookmark_service.get_bookmark_tickets(user_id, db)


@router.put("/bookmark/{user_id}")
async def bookmark_ticket(user_id: int, ticket_id: int, db: AsyncSession = Depends(get_session)):
    return await bookmark_service.addBookmark(user_id, ticket_id, db)
