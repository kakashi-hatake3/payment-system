from pydantic import BaseModel
from decimal import Decimal
from datetime import datetime


class PaymentBase(BaseModel):
    transaction_id: str
    account_id: int
    amount: Decimal


class PaymentCreate(PaymentBase):
    pass


class PaymentResponse(PaymentBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True


class WebhookPayload(BaseModel):
    transaction_id: str
    user_id: int
    account_id: int
    amount: Decimal
    signature: str
