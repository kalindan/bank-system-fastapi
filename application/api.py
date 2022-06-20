from fastapi import FastAPI, Depends, Body
from .database import create_db_and_tables, get_session, Session
from .models import Account, AccountRead, Customer, CustomerWrite, CustomerRead
from .schemas import Limits
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
    return crud_customer.create(session=session, customer=db_customer)


@app.get("/customers/{customer_id}", response_model=CustomerRead)
def customer_info(customer_id: int, session: Session = Depends(get_session)):
    return crud_customer.read(session=session, customer_id=customer_id)


@app.post("/customers/{customer_id}", response_model=CustomerRead)
def login_customer(customer_id: int, session: Session = Depends(get_session)):
    pass


@app.delete("/customers/{customer_id}")
def delete_customer(customer_id: int, session: Session = Depends(get_session)):
    return crud_customer.delete(session=session, customer_id=customer_id)


@app.post("/accounts", response_model=AccountRead)
def register_account(session: Session = Depends(get_session)):
    customer_id: int = 1  # temporary until authentication is added
    return crud_account.create(session=session, customer_id=customer_id)


@app.delete("/accounts/{account_id}")
def delete_account(account_id: int, session: Session = Depends(get_session)):
    return crud_account.delete(session=session, account_id=account_id)


@app.get("/accounts/{account_id}", response_model=AccountRead)
def get_account(account_id: int, session: Session = Depends(get_session)):
    return crud_account.read(session=session, account_id=account_id)


@app.post("/accounts/{account_id}/limits")
def set_limits(account_id: int, limits: Limits, session: Session = Depends(get_session)):
    return crud_account.update_limits(session=session, account_id=account_id, limits=limits)


@app.put("/accounts/{account_id}/withdrawal")
def withdraw_money(account_id: int, amount: int = Body(), session: Session = Depends(get_session)):
    account = crud_account.read(session=session, account_id=account_id)
    # to do "if account.balance"


@app.put("/accounts/{account_id}/deposit")
def deposit_money(account_id: int, amount: int = Body(), session: Session = Depends(get_session)):
    pass


# @app.put("/accounts/{account_id}/transfer")
# def transfer_money(account_id: int, account_to: Account, amount:int= Body()):
#     pass
