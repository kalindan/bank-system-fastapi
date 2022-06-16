from sqlmodel import Field, SQLModel

class CustomerBase(SQLModel):
    name: str = Field(index=True)

class CustomerWrite(CustomerBase):
    password: str = Field(min_length=10)

class CustomerDB(CustomerBase, table=True):
    id: int | None = Field(default=None, primary_key=True)
    hashed_password: str = Field(default=None)
    
class CustomerRead(CustomerBase):
    id: int