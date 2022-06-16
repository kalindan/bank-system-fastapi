from fastapi import FastAPI
from .database import create_db_and_tables
from .models import CustomerDB, CustomerWrite, CustomerRead
from .utils import get_password_hash
from .crud import crud_customer
app = FastAPI()

@app.on_event("startup")
def on_startup():
    create_db_and_tables()
    
@app.post("/customers", response_model=CustomerRead)
def register_customer(customer: CustomerWrite):
    db_customer = CustomerDB.from_orm(customer)
    db_customer.hashed_password = get_password_hash(customer.password)
    created_customer = crud_customer.create(db_customer)
    return created_customer
    
@app.get("/customers/{customer_id}", response_model=CustomerRead)
def customer_info(customer_id:int):
    customer_from_db = crud_customer.read(customer_id)
    return customer_from_db

@app.delete("/customers/{customer_id}")
def delete_customer(customer_id:int):
    return crud_customer.delete(customer_id)

# @app.post("/customers/{customer_id}/accounts")
# def register_account(customer: Customer):
#     pass

# @app.delete("/customers/{customer_id}/accounts/{account_id}")
# def delete_account(account: Account):
#     pass

# @app.get("/customers/{customer_id}/accounts/{account_id}")
# def get_account_info(account: Account):
#     pass

# @app.post("/customers/{customer_id}/accounts/{account_id}/limits")
# def set_limits(account: Account, limits: Limits):
#     pass

# @app.get("/customers/{customer_id}/accounts/{account_id}/limits")
# def get_limits(account: Account, limits: Limits):
#     pass

# @app.put("/customers/{customer_id}/accounts/{account_id}/transfer")
# def transfer_money(account_from: Account, account_to: Account, amount:int= Body()):
#     pass

# @app.put("/customers/{customer_id}/accounts/{account_id}/withdrawal")
# def withdraw_money(account: Account, amount:int= Body()):
#     pass

# @app.put("/customers/{customer_id}/accounts/{account_id}/deposit")
# def deposit_money(account: Account, amount:int= Body()):
#     pass


