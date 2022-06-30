from datetime import datetime
from .base_models import TransactionBase, AccountBase, CustomerBase
from .transaction_model import TransactionType


class TransactionRead(TransactionBase):
    transaction_type: TransactionType
    date: datetime


class AccountRead(AccountBase):
    id: int
    balance: float
    transactions: list["TransactionRead"] = []


class CustomerRead(CustomerBase):
    id: int
    accounts: list["AccountRead"] = []
