from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.orm import selectinload
from app.database import get_db
from app.models import User, Account, Payment
from app.schemas.user import UserResponse
from app.schemas.account import AccountResponse
from app.schemas.payment import PaymentResponse
from app.api.deps import get_current_user

router = APIRouter(prefix="/users", tags=["users"])


@router.get("/me", response_model=UserResponse)
async def get_current_user_info(
    current_user: User = Depends(get_current_user)
):
    return current_user


@router.get("/me/accounts", response_model=List[AccountResponse])
async def get_user_accounts(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    result = await db.execute(
        select(Account)
        .where(Account.user_id == current_user.id)
    )
    accounts = result.scalars().all()
    return accounts


@router.get("/me/payments", response_model=List[PaymentResponse])
async def get_user_payments(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    result = await db.execute(
        select(Payment)
        .join(Account)
        .where(Account.user_id == current_user.id)
        .order_by(Payment.created_at.desc())
    )
    payments = result.scalars().all()
    return payments
