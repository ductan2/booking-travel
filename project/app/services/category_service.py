from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.exc import NoResultFound
from sqlalchemy.ext.asyncio import AsyncSession

from app.models import Category
from app.schemas.category_schema import CategoryCreate
from app.utils.cloudinary import upload_image


async def get_category_by_name(name: str, db: AsyncSession):
    result = await db.execute(select(Category).filter(Category.name == name))
    return result.scalar_one_or_none()


async def get_category_by_id(category_id: int, db: AsyncSession):
    result = await db.execute(select(Category).filter(Category.id == category_id))
    return result.scalar_one_or_none()


async def get_all_categories(db: AsyncSession):
    result = await db.execute(select(Category))
    return result.scalars().all()


async def create_category(category: CategoryCreate, db: AsyncSession):
    if await get_category_by_name(category.name, db):
        raise HTTPException(status_code=400, detail="Category already exists")
    url_image = await upload_image(category.image)
    db_category = Category(name=category.name, description=category.description, image=url_image)
    db.add(db_category)
    await db.commit()
    await db.refresh(db_category)
    return db_category


async def update_category(category_id: int, category: CategoryCreate, db: AsyncSession):
    db_category = await get_category_by_id(category_id, db)
    if not db_category:
        raise HTTPException(status_code=404, detail="Category not found")
    if category.name:
        db_category.name = category.name
    if category.description:
        db_category.description = category.description

    await db.commit()
    await db.refresh(db_category)
    return db_category


async def delete_category(category_id: int, db: AsyncSession):
    db_category = await get_category_by_id(category_id, db)
    if not db_category:
        raise HTTPException(status_code=404, detail="Category not found")

    await db.delete(db_category)
    await db.commit()

    return db_category
