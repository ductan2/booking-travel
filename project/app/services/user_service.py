from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models import User
from app.schemas.user_schema import UserCreate, UserUpdate, UserLogin , UserPassword
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


async def get_user_by_email(email: str, db: AsyncSession):
    result = await db.execute(select(User).filter(User.email == email))
    return result.scalar_one_or_none()


async def get_user_by_username(username: str, db: AsyncSession):
    result = await db.execute(select(User).filter(User.username == username))
    return result.scalar_one_or_none()


async def get_user_by_id(user_id: int, db: AsyncSession):
    result = await db.execute(select(User).filter(User.id == user_id))
    return result.scalar_one_or_none()


async def create_user(user: UserCreate, db: AsyncSession):
    hashed_password = pwd_context.hash(user.password)
    db_user = User(email=user.email, username=user.username, password=hashed_password)
    db.add(db_user)
    await db.commit()
    await db.refresh(db_user)
    return db_user


async def login_user(user: UserLogin, db: AsyncSession):
    db_user = await get_user_by_email(user.account, db) or await get_user_by_username(user.account, db)
    if not db_user:
        return False
    if not pwd_context.verify(user.password, db_user.password):
        return False
    return db_user


async def update_user(user_id: int, user: UserUpdate, db: AsyncSession):
    db_user = await get_user_by_id(user_id, db)
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")
    if (user.email is not None and get_user_by_email(user.email, db)
            or user.username is not None and get_user_by_username(user.username, db)):
        raise HTTPException(status_code=400, detail="Username or Email already registered")

    user_data = user.dict(exclude_unset=True)

    if 'password' in user_data:
        user_data['password'] = pwd_context.hash(user_data['password'])

    for key, value in user_data.items():
        setattr(db_user, key, value)

    await db.commit()
    await db.refresh(db_user)
    return db_user


async def update_password(user_id: int,updatePassword: UserPassword, db: AsyncSession):
    db_user = await get_user_by_id(user_id, db)
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")
    if not pwd_context.verify(old_password, db_user.password):
        raise HTTPException(status_code=400, detail="Old password incorrect")
    db_user.password = pwd_context.hash(password)
    await db.commit()
    return db_user

