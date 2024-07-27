from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session

from app.database import get_session
from app.schemas.category_schema import CategoryBase, CategoryCreate, CategoryUpdate
from app.services import category_service

router = APIRouter()


@router.post("/", response_model=CategoryBase)
async def create_category(category: CategoryCreate, db: Session = Depends(get_session)):
    if await category_service.get_category_by_name(category.name, db):
        raise HTTPException(status_code=400, detail="Category already exists")
    return await category_service.create_category(category, db)


@router.get("/",response_model=List[CategoryBase])
async def read_categories(db: Session = Depends(get_session)):
    return await category_service.get_all_categories(db)


@router.delete("/{category_id}", response_model=CategoryBase)
async def delete_category(category_id: int, db: Session = Depends(get_session)):
    try:
        return await category_service.delete_category(category_id, db)
    except HTTPException as e:
        raise HTTPException(status_code=e.status_code, detail=e.detail)


@router.put("/{category_id}", response_model=CategoryBase)
async def update_category(category_id: int, category: CategoryUpdate, db: Session = Depends(get_session)):
    try:
        return await category_service.update_category(category_id, category, db)
    except HTTPException as e:
        raise HTTPException(status_code=e.status_code, detail=e.detail)


@router.get("/{category_id}", response_model=CategoryBase)
async def read_category(category_id: int):
    try:
        return await category_service.get_category_by_id(category_id)
    except HTTPException as e:
        raise HTTPException(status_code=e.status_code, detail=e.detail)
