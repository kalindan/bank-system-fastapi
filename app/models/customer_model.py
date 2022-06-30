from sqlmodel import Field, Relationship
from typing import TYPE_CHECKING
from fastapi import HTTPException
from passlib.context import CryptContext  # type:ignore
from ..models.read_models import CustomerRead, CustomerResponse
from ..db import Session
from .base_models import CustomerBase

if TYPE_CHECKING:
    from .account_model import Account

pwd_context = CryptContext(schemes=["bcrypt"])


class CustomerWrite(CustomerBase):
    password: str = Field(min_length=10)


class Customer(CustomerBase, table=True):
    id: int | None = Field(default=None, primary_key=True)
    hashed_password: str = Field(default=None)
    accounts: list["Account"] = Relationship(back_populates="customer")

    def verify_password(self, password: str) -> bool:
        return pwd_context.verify(password, self.hashed_password)

    def hash_password(self, password: str):
        self.hashed_password = pwd_context.hash(password)
        return self

    def get_response_model(self, status: str, message: str):
        customer_response = CustomerResponse.from_orm(self)
        customer_response.status = status
        customer_response.message = message
        return customer_response

    def db_create(self, session: Session):
        session.add(self)
        session.commit()
        session.refresh(self)
        return self

    def db_read(self, session: Session):
        customer = session.get(Customer, self.id)
        if not customer:
            raise HTTPException(status_code=404, detail="Customer not found")
        self = customer
        return self

    def db_delete(self, session: Session):
        customer = session.get(Customer, self.id)
        if not customer:
            raise HTTPException(status_code=404, detail="Customer not found")
        session.delete(customer)
        session.commit()
        return
