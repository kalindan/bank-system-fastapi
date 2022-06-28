from datetime import datetime
from fastapi import HTTPException
from sqlmodel import select
import enum
from sqlmodel import Field, Relationship, SQLModel, Column, Enum
from typing import TYPE_CHECKING
from ..db import Session
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

    def db_create(self, session: Session):
        account = session.get(Account, self.account_id)
        if not account:
            raise HTTPException(status_code=404, detail="Account not found")
        session.add(self)
        session.commit()
        session.refresh(self)
        return self
    
    def db_read_all(self, session: Session):
        transactions = session.exec(select(Transaction).where(Transaction.account_id==self.account_id))
        return transactions
    
    def db_delete_all(self, session: Session):
        transactions = session.exec(select(Transaction).where(Transaction.account_id==self.account_id))
        for transaction in transactions:
            session.delete(transaction)
        session.commit()
        return 
    
class TransactionWrite(TransactionBase):
    pass