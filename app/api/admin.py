from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, delete
from sqlalchemy.orm import selectinload
from app.database import get_db
from app.models import User, Admin, Account
from app.schemas.user import UserCreate, UserUpdate, UserResponse, UserWithAccounts
from app.schemas.admin import AdminResponse
from app.core.security import get_password_hash
from app.api.deps import get_current_admin

router = APIRouter(prefix="/admin", tags=["admin"])


@router.get("/me", response_model=AdminResponse)
async def get_current_admin_info(
        current_admin: Admin = Depends(get_current_admin)
):
    return current_admin


@router.post("/users", response_model=UserResponse)
async def create_user(
        user_data: UserCreate,
        current_admin: Admin = Depends(get_current_admin),
        db: AsyncSession = Depends(get_db)
):
    # Проверяем существование пользователя
    result = await db.execute(select(User).where(User.email == user_data.email))
    if result.scalar_one_or_none():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User with this email already exists"
        )

    user = User(
        email=user_data.email,
        full_name=user_data.full_name,
        hashed_password=get_password_hash(user_data.password)
    )
    db.add(user)
    await db.commit()
    await db.refresh(user)
    return user


@router.get("/users", response_model=List[UserWithAccounts])
async def get_all_users(
        current_admin: Admin = Depends(get_current_admin),
        db: AsyncSession = Depends(get_db)
):
    result = await db.execute(
        select(User).options(selectinload(User.accounts))
    )
    users = result.scalars().unique().all()
    return users


@router.get("/users/{user_id}", response_model=UserWithAccounts)
async def get_user(
        user_id: int,
        current_admin: Admin = Depends(get_current_admin),
        db: AsyncSession = Depends(get_db)
):
    result = await db.execute(
        select(User)
        .options(selectinload(User.accounts))
        .where(User.id == user_id)
    )
    user = result.scalar_one_or_none()

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )

    return user


@router.put("/users/{user_id}", response_model=UserResponse)
async def update_user(
        user_id: int,
        user_data: UserUpdate,
        current_admin: Admin = Depends(get_current_admin),
        db: AsyncSession = Depends(get_db)
):
    result = await db.execute(select(User).where(User.id == user_id))
    user = result.scalar_one_or_none()

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )

    if user_data.email is not None:
        user.email = user_data.email
    if user_data.full_name is not None:
        user.full_name = user_data.full_name
    if user_data.password is not None:
        user.hashed_password = get_password_hash(user_data.password)

    await db.commit()
    await db.refresh(user)
    return user


@router.delete("/users/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(
        user_id: int,
        current_admin: Admin = Depends(get_current_admin),
        db: AsyncSession = Depends(get_db)
):
    result = await db.execute(select(User).where(User.id == user_id))
    user = result.scalar_one_or_none()

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )

    await db.delete(user)
    await db.commit()
