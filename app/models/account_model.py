from datetime import datetime
from fastapi import HTTPException, status
from sqlmodel import Field, Relationship
from typing import TYPE_CHECKING

from app.models.read_models import AccountResponse
from ..db import Session
from .enums import TransactionType

from .customer_model import Customer
from .limits_model import Limits
from .base_models import AccountBase

if TYPE_CHECKING:
    from .customer_model import Customer
    from .transaction_model import Transaction


class Account(AccountBase, table=True):
    id: int | None = Field(default=None, primary_key=True)
    balance: float = Field(default=0.0)
    customer_id: int | None = Field(default=None, foreign_key="customer.id")
    customer: "Customer" = Relationship(back_populates="accounts")
    transactions: list["Transaction"] = Relationship(back_populates="account")

    def check_balance(self, amount: float):
        if self.balance < amount:
            raise HTTPException(
                status_code=status.HTTP_406_NOT_ACCEPTABLE,
                detail="Not sufficient balance",
            )
        return self

    def check_daily_withdrawals(self):
        withdrawals_today = len(
            [
                transaction
                for transaction in self.transactions
                if transaction.date.date() == datetime.now().date()
                and transaction.transaction_type == TransactionType.WITHDRAWAL
            ]
        )
        if self.num_of_withdrawals <= withdrawals_today:
            raise HTTPException(
                status_code=status.HTTP_406_NOT_ACCEPTABLE,
                detail="No more allowed withdrawals today",
            )
        return self

    def check_amount_withdrawn(self, amount: float):
        withdrawn_today = sum(
            [
                transaction.amount
                for transaction in self.transactions
                if transaction.date.date() == datetime.now().date()
                and transaction.transaction_type == TransactionType.WITHDRAWAL
            ]
        )
        if amount > self.daily_limit - withdrawn_today:
            raise HTTPException(
                status_code=status.HTTP_406_NOT_ACCEPTABLE,
                detail="Desired amount over allowed daily limit",
            )
        return self

    def set_customer_id(self, id: int | None):
        self.customer_id = id
        return self

    def get_response_model(self, status: int, message: str):
        account_response = AccountResponse.from_orm(self)
        account_response.status = status
        account_response.message = message
        return account_response

    def db_create(self, session: Session):
        customer = session.get(Customer, self.customer_id)
        if not customer:
            raise HTTPException(status_code=404, detail="Customer not found")
        session.add(self)
        session.commit()
        session.refresh(self)
        return self

    def db_read(self, session: Session):
        account = session.get(Account, self.id)
        if not account:
            raise HTTPException(status_code=404, detail="Account not found")
        self = account
        return self

    def db_update_balance(self, session: Session, amount: float):
        account = session.get(Account, self.id)
        if not account:
            raise HTTPException(status_code=404, detail="Account not found")
        self = account
        self.balance += amount
        session.add(self)
        session.commit()
        session.refresh(self)
        return self

    def db_update_limits(self, session: Session, limits: Limits):
        account = session.get(Account, self.id)
        if not account:
            raise HTTPException(status_code=404, detail="Account not found")
        self = account
        self.daily_limit = limits.daily_limit
        self.num_of_withdrawals = limits.num_of_withdrawals
        session.add(self)
        session.commit()
        session.refresh(self)
        return self

    def db_delete(self, session: Session):
        account = session.get(Account, self.id)
        if not account:
            raise HTTPException(status_code=404, detail="Account not found")
        session.delete(account)
        session.commit()
        return self

    def db_check_ownership(self, customer_id: int | None, session: Session):
        account = session.get(Account, self.id)
        if not account:
            raise HTTPException(status_code=404, detail="Account not found")
        if account.customer_id != customer_id:
            raise HTTPException(
                status_code=401, detail="Not authorized to this account"
            )
        self = account
        return self


class AccountWrite(AccountBase):
    pass
