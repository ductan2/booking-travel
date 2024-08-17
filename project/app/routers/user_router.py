from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.database import get_session
from app.schemas.user_schema import UserCreate, UserBase, UserUpdate, UserLogin, UserUpdatePass
from app.services import user_service
from passlib.context import CryptContext

router = APIRouter()

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


@router.post("/register", response_model=UserBase)
async def register_user(user: UserCreate, db: AsyncSession = Depends(get_session)):
    if await user_service.get_user_by_email(user.email, db) or await user_service.get_user_by_username(user.username, db):
        raise HTTPException(status_code=400, detail="Username or Email already registered")
    return await user_service.create_user(user, db)


@router.post("/login", response_model=UserBase)
async def login_user(user: UserLogin, db: AsyncSession = Depends(get_session)):
    db_user = await user_service.login_user(user, db)
    if not db_user:
        raise HTTPException(status_code=400, detail="Account or Password incorrect")
    return db_user


@router.get("/get/{user_id}", response_model=UserBase)
async def get_user(user_id: int, db: AsyncSession = Depends(get_session)):
    user = await user_service.get_user_by_id(user_id, db)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user


@router.put("/update/{user_id}", response_model=UserBase)
async def update_user(user_id: int, user: UserUpdate, db: AsyncSession = Depends(get_session)):
    updated_user = await user_service.update_user(user_id, user, db)
    if not updated_user:
        raise HTTPException(status_code=404, detail="User not found or could not be updated")
    return updated_user


@router.put("/update/password/{user_id}")
async def update_password(user_id: int, user_update: UserUpdatePass, db: AsyncSession = Depends(get_session)):
    db_user = await user_service.get_user_by_id(user_id, db)
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")

    if not pwd_context.verify(user_update.old_password, db_user.password):
        raise HTTPException(status_code=400, detail="Old password incorrect")

    db_user.password = pwd_context.hash(user_update.password)
    await db.commit()
    await db.refresh(db_user)

    return db_user
