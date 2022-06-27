from sqlmodel import Field, Relationship, SQLModel
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from .customer_model import Customer
    from .transaction_model import Transaction

class AccountBase(SQLModel):
    balance: float = Field(default=0.0)
    daily_limit: float = Field(default=0.0)
    num_of_withdrawals: int = Field(default=0)


class Account(AccountBase, table=True):
    id: int | None = Field(default=None, primary_key=True)
    customer_id: int = Field(default=None, foreign_key="customer.id")
    customer: "Customer" = Relationship(back_populates="accounts")
    transactions: list["Transaction"] = Relationship(back_populates="account")

