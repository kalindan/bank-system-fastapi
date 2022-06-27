from datetime import datetime
import enum
from sqlmodel import Field, Relationship, SQLModel, Column, Enum
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from .account_model import Account

class TransactionType(enum.Enum):
    WITHDRAWAL = "withdrawal"
    DEPOSIT = "deposit"
    TRANSFER = "transfer"
    NONE = "none"

class TransactionBase(SQLModel):
    amount: float = Field(default = 0.0)
    
class Transaction(TransactionBase, table=True):
    id: int | None = Field(default=None, primary_key=True)
    transaction_type: TransactionType = Field(default=TransactionType.NONE, sa_column=Column(Enum(TransactionType)))
    account_id: int = Field(default=None, foreign_key="account.id")
    account: "Account" = Relationship(back_populates="transactions")
    date: datetime = Field(default = datetime.now())

class TransactionWrite(TransactionBase):
    pass