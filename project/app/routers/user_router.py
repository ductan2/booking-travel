from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session

from app.database import get_session

from app.schemas.user_schema import UserCreate, UserBase, UserUpdate, UserLogin
from app.services import user_service

router = APIRouter()


@router.get("/{user_id}")
async def read_user(user_id: str):
    return {"user_id": user_id}


@router.post("/register", response_model=UserBase)
async def register_user(user: UserCreate, db: Session = Depends(get_session)):
    if await user_service.get_user_by_email(user.email, db) or await user_service.get_user_by_username(user.username,
                                                                                                       db):
        raise HTTPException(status_code=400, detail="Username or Email already registered")
    return await user_service.create_user(user, db)


@router.post("/login", response_model=UserBase)
async def login_user(user: UserLogin, db: Session = Depends(get_session)):
    db_user = await user_service.login_user(user, db)
    if not db_user:
        raise HTTPException(status_code=400, detail="Account or Password incorrect")
    return db_user


@router.put("/update/{user_id}", response_model=UserBase)
async def update_user(user_id: int, user: UserUpdate, db: Session = Depends(get_session)):
    try:
        updated_user = await user_service.update_user(user_id, user, db)
        return updated_user
    except HTTPException as e:
        raise HTTPException(status_code=e.status_code, detail=e.detail)
