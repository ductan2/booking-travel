from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models import Location
from app.schemas.location_schema import LocationUpdate, LocationCreate


async def get_location_by_id(location_id: int, db: AsyncSession):
    location = await db.get(Location, location_id)
    if not location:
        raise HTTPException(status_code=404, detail="Location not found")
    return location


async def get_all_locations(db: AsyncSession):
    result = await db.execute(select(Location))
    return result.scalars().all()


async def create_location(location: LocationCreate, db: AsyncSession):
    existing = await db.execute(select(Location).filter(Location.name == location.name))
    if existing.scalar_one_or_none():
        raise HTTPException(status_code=400, detail="Location already exists")
    db_location = Location(**location.dict())
    db.add(db_location)
    await db.commit()
    await db.refresh(db_location)
    return db_location


async def update_location(location_id: int, location: LocationUpdate, db: AsyncSession):
    db_location = await get_location_by_id(location_id, db)
    location_data = location.dict(exclude_unset=True)
    for key, value in location_data.items():
        setattr(db_location, key, value)
    await db.commit()
    await db.refresh(db_location)
    return db_location


async def delete_location(location_id: int, db: AsyncSession):
    db_location = await get_location_by_id(location_id, db)
    await db.delete(db_location)
    await db.commit()
    return db_location
