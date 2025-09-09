from pydantic import BaseModel
from decimal import Decimal


class AccountBase(BaseModel):
    user_id: int


class AccountCreate(AccountBase):
    pass


class AccountResponse(BaseModel):
    id: int
    user_id: int
    balance: Decimal

    class Config:
        from_attributes = True
