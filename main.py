from typing import List
from fastapi import FastAPI, Body
from pydantic import BaseModel, Field
import uvicorn  #type:ignore

app = FastAPI()

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
    

customers : List[Customer] = []

@app.post("/register-customer")
def register_customer(new_customer: Customer):
    customers.append(new_customer)
    return "Customer succesfully registered"

@app.post("/create-account")
def create_account(new_account: Account, customer: Customer):
    pass

@app.post("/set-limits")
def set_limits(account: Account, limits: Limits):
    pass

@app.get("/get-balance")
def get_balance(account: Account):
    pass

@app.get("/get-limits")
def get_limits(account: Account, limits: Limits):
    pass

@app.put("/transfer-money")
def transfer_money(account_from: Account, account_to: Account, amount:int= Body()):
    pass

@app.put("/withdraw-money")
def withdraw_money(account: Account, amount:int= Body()):
    pass

@app.put("/deposit-money")
def deposit_money(account: Account, amount:int= Body()):
    pass

@app.delete("/delete-account")
def delete_account(account: Account):
    pass

@app.delete("/delete-customer")
def delete_customer(customer: Customer):
    pass

if __name__ == "__main__":
    uvicorn.run("main:app",reload=True)
