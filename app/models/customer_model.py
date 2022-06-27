from sqlmodel import Field, Relationship, SQLModel
from pydantic import EmailStr
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from .account_model import Account

class CustomerBase(SQLModel):
    name: str = Field(index=True)
    email: EmailStr = Field(index=True)
    
class CustomerWrite(CustomerBase):
    password: str = Field(min_length=10)

class Customer(CustomerBase, table=True):
    id: int | None = Field(default=None, primary_key=True)
    hashed_password: str = Field(default=None)
    accounts: list["Account"] = Relationship(back_populates="customer")

