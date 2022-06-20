from pydantic import BaseModel, Field


class Customer(BaseModel):
    email: str
    password: str = Field(min_length=10)


class Account(BaseModel):
    number: int
    balance: float


class Limits(BaseModel):
    daily_limit: float
    num_of_withdrawals: int
