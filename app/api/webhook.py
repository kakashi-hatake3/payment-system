from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.database import get_db
from app.models import User, Account, Payment
from app.schemas.payment import WebhookPayload
from app.core.webhook_security import verify_signature

router = APIRouter(prefix="/webhook", tags=["webhook"])


@router.post("/payment")
async def process_payment_webhook(
        payload: WebhookPayload,
        db: AsyncSession = Depends(get_db)
):
    # 1. Проверяем подпись
    if not verify_signature(
            payload.transaction_id,
            payload.user_id,
            payload.account_id,
            payload.amount,
            payload.signature
    ):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid signature"
        )

    # 2. Проверяем существование пользователя
    user_result = await db.execute(select(User).where(User.id == payload.user_id))
    user = user_result.scalar_one_or_none()

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )

    # 3. Проверяем уникальность транзакции
    payment_result = await db.execute(
        select(Payment).where(Payment.transaction_id == payload.transaction_id)
    )
    existing_payment = payment_result.scalar_one_or_none()

    if existing_payment:
        return {"status": "already_processed", "transaction_id": payload.transaction_id}

    # 4. Получаем или создаем счет
    account_result = await db.execute(
        select(Account)
        .where(Account.id == payload.account_id)
        .where(Account.user_id == payload.user_id)
    )
    account = account_result.scalar_one_or_none()

    if not account:
        # Создаем новый счет
        account = Account(
            id=payload.account_id,
            user_id=payload.user_id,
            balance=0
        )
        db.add(account)
        await db.flush()

    # 5. Создаем платеж
    payment = Payment(
        transaction_id=payload.transaction_id,
        account_id=account.id,
        amount=payload.amount
    )
    db.add(payment)

    # 6. Обновляем баланс
    account.balance += payload.amount

    await db.commit()

    return {
        "status": "success",
        "transaction_id": payload.transaction_id,
        "new_balance": float(account.balance)
    }
