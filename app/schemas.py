from pydantic import BaseModel, Field

class Customer(BaseModel):
    email:str
    password:str = Field(min_length=10)
    
class Account(BaseModel):
    number:int
    pin_code:int
    balance:float

class Limits(BaseModel):
    daily_limit:float
    max_limit:float