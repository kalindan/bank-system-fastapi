from fastapi import status
from datetime import datetime

from sqlmodel import Field
from .base_models import TransactionBase, AccountBase, CustomerBase
from .enums import TransactionType


class TransactionRead(TransactionBase):
    transaction_type: TransactionType
    date: datetime


class AccountRead(AccountBase):
    id: int
    balance: float
    transactions: list["TransactionRead"] = []


class AccountResponse(AccountRead):
    status: str = Field(default="")
    message: str = Field(default="")


class CustomerRead(CustomerBase):
    id: int
    accounts: list["AccountRead"] = []


class CustomerResponse(CustomerBase):
    status: str = Field(default="")
    message: str = Field(default="")
