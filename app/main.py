from fastapi import FastAPI, Body
from fastapi.security import OAuth2PasswordBearer
import uvicorn  #type:ignore
from schemas import Customer,Account,Limits

app = FastAPI()

@app.post("/customer")
def register_customer(customer: Customer):
    return "Customer succesfully registered"

@app.get("/customer/{customer_id} ")
def customer_info(customer: Customer):
    pass

@app.delete("/customer/{customer_id}")
def delete_customer(customer: Customer):
    pass

@app.post("/customer/{customer_id}/account")
def register_account(customer: Customer):
    pass

@app.delete("/customer/{customer_id}/account/{account_id}")
def delete_account(account: Account):
    pass

@app.get("/customer/{customer_id}/account/{account_id}")
def get_account_info(account: Account):
    pass

@app.post("/customer/{customer_id}/account/{account_id}/limits")
def set_limits(account: Account, limits: Limits):
    pass

@app.get("/customer/{customer_id}/account/{account_id}/limits")
def get_limits(account: Account, limits: Limits):
    pass

@app.put("/customer/{customer_id}/account/{account_id}/transfer")
def transfer_money(account_from: Account, account_to: Account, amount:int= Body()):
    pass

@app.put("/customer/{customer_id}/account/{account_id}/withdrawal")
def withdraw_money(account: Account, amount:int= Body()):
    pass

@app.put("/customer/{customer_id}/account/{account_id}/deposit")
def deposit_money(account: Account, amount:int= Body()):
    pass


if __name__ == "__main__":
    uvicorn.run("main:app",reload=True)
