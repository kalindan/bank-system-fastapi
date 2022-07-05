from sqlmodel import Field, SQLModel
from pydantic import EmailStr


class CustomerBase(SQLModel):
    name: str = Field()
    email: EmailStr = Field()


class AccountBase(SQLModel):
    daily_limit: float = Field(default=0.0, gt=0)
    num_of_withdrawals: int = Field(default=0, gt=0)


class TransactionBase(SQLModel):
    amount: float = Field(default=0.0)
