from fastapi import APIRouter, Depends
from app.db import get_session, Session, crud_customer
from app.models import  Customer, CustomerWrite, CustomerRead
from app.utils import get_password_hash

router = APIRouter(prefix="/customers",
                   tags=["customers"])

@router.post("/", response_model=CustomerRead)
def register_customer(customer: CustomerWrite, session: Session = Depends(get_session)):
    db_customer = Customer.from_orm(customer)
    db_customer.hashed_password = get_password_hash(customer.password)
    return crud_customer.create(session=session, customer=db_customer)


@router.get("/{customer_id}", response_model=CustomerRead)
def customer_info(customer_id: int, session: Session = Depends(get_session)):
    return crud_customer.read(session=session, customer_id=customer_id)


@router.post("/{customer_id}", response_model=CustomerRead)
def login_customer(customer_id: int, session: Session = Depends(get_session)):
    pass


@router.delete("/{customer_id}")
def delete_customer(customer_id: int, session: Session = Depends(get_session)):
    return crud_customer.delete(session=session, customer_id=customer_id)
