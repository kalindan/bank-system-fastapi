from sqlmodel import Field, Relationship, SQLModel


class CustomerBase(SQLModel):
    name: str = Field(index=True)


class CustomerWrite(CustomerBase):
    password: str = Field(min_length=10)


class Customer(CustomerBase, table=True):
    id: int | None = Field(default=None, primary_key=True)
    hashed_password: str = Field(default=None)
    accounts: list["Account"] = Relationship(back_populates="customer")


class AccountBase(SQLModel):
    balance: float = Field(default=0)
    daily_limit: float = Field(default=0)
    num_of_withdrawals: int = Field(default=0)


class Account(AccountBase, table=True):
    id: int | None = Field(default=None, primary_key=True)
    customer_id: int = Field(default=None, foreign_key="customer.id")
    customer: Customer = Relationship(back_populates="accounts")


class AccountRead(AccountBase):
    id: int


class CustomerRead(CustomerBase):
    id: int
    accounts: list[AccountRead] = []
