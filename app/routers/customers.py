from fastapi import APIRouter, Depends
from app.db import get_session, Session
from app.models import  Customer, CustomerWrite, CustomerRead

router = APIRouter(prefix="/customers",
                   tags=["customers"])

@router.post("/")
def register_customer(customer_write: CustomerWrite, session: Session = Depends(get_session)):
    customer_db = Customer.from_orm(customer_write)\
                          .hash_password(customer_write.password)\
                          .db_create(session=session)
    customer_read = CustomerRead.from_orm(customer_db)
    return {"status":"success",
            "message": f"Customer {customer_read.id} successfully created",
            "customer_info":customer_read}


@router.get("/{customer_id}")
def customer_info(customer_id: int, session: Session = Depends(get_session)):
    customer = Customer(id=customer_id).db_read(session=session)
    return {"status":"success",
            "message": f"Customer {customer_id} successfully loaded",
            "customer_info":customer}


@router.post("/{customer_id}", response_model=CustomerRead)
def login_customer(customer_id: int, session: Session = Depends(get_session)):
    pass


@router.delete("/{customer_id}")
def delete_customer(customer_id: int, session: Session = Depends(get_session)):
    Customer(id=customer_id).db_delete(session=session)
    return {"status":"success",
            "message": f"Customer {customer_id} successfully deleted"}