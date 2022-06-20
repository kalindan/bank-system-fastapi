from fastapi import FastAPI, Depends
from .database import create_db_and_tables, get_session, Session
from .models import Account, Customer, CustomerWrite, CustomerRead
from .utils import get_password_hash
from .crud import crud_customer, crud_account

app = FastAPI()

@app.on_event("startup")
def on_startup():
    create_db_and_tables()
    
@app.post("/customers", response_model=CustomerRead)
def register_customer(customer: CustomerWrite, session: Session = Depends(get_session)):
    db_customer = Customer.from_orm(customer)
    db_customer.hashed_password = get_password_hash(customer.password)
    registered_customer = crud_customer.create(session = session, customer = db_customer)
    return registered_customer
    
@app.get("/customers/{customer_id}", response_model=CustomerRead)
def customer_info(customer_id:int, session: Session = Depends(get_session)):
    customer_from_db = crud_customer.read(session = session, customer_id = customer_id)
    return customer_from_db

@app.post("/customers/{customer_id}", response_model=CustomerRead)
def login_customer(customer_id:int, session: Session = Depends(get_session)):
    pass

@app.delete("/customers/{customer_id}")
def delete_customer(customer_id:int, session: Session = Depends(get_session)):
    return crud_customer.delete(session = session, customer_id = customer_id)

@app.post("/accounts", response_model=Account)
def register_account(session: Session = Depends(get_session)):
    customer_id:int = 1 # temporary until authentication is added
    account = crud_account.create(session = session, customer_id=customer_id)
    return account

@app.delete("/accounts/{account_id}")
def delete_account(account_id:int, session: Session = Depends(get_session)):
    return crud_account.delete(session=session, account_id=account_id)

@app.get("/accounts/{account_id}")
def get_account(account_id:int, session: Session = Depends(get_session)):
    pass

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


