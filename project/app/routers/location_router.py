from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_session
from app.schemas.location_schema import Location, LocationCreate, LocationUpdate
from app.services import location_service

router = APIRouter()


@router.post("/", response_model=Location)
async def create_location(location: LocationCreate, db: AsyncSession = Depends(get_session)):
    return await location_service.create_location(location, db)


@router.get("/", response_model=List[Location])
async def get_all_locations(db: AsyncSession = Depends(get_session)):
    return await location_service.get_all_locations(db)


@router.get("/{location_id}", response_model=Location)
async def get_location_by_id(location_id: int, db: AsyncSession = Depends(get_session)):
    return await location_service.get_location_by_id(location_id, db)


@router.put("/{location_id}", response_model=Location)
async def update_location(location_id: int, location: LocationUpdate, db: AsyncSession = Depends(get_session)):
    return await location_service.update_location(location_id, location, db)


@router.delete("/{location_id}", response_model=Location)
async def delete_location(location_id: int, db: AsyncSession = Depends(get_session)):
    return await location_service.delete_location(location_id, db)
