from fastapi import APIRouter, Depends, status
from fastapi.responses import JSONResponse
from app.db import get_session, Session
from app.models import Customer, CustomerWrite, CustomerRead

router = APIRouter(prefix="/customers", tags=["customers"])


@router.post("/")
def register_customer(customer_write: CustomerWrite, session: Session = Depends(get_session)):
    customer = Customer.from_orm(customer_write).hash_password(customer_write.password).db_create(session=session).get_read_model()
    return JSONResponse(
        status_code=status.HTTP_201_CREATED, content={"message": f"Customer {customer.id} successfully created", "customer_info": customer.dict()}
    )


@router.get("/{customer_id}")
def customer_info(customer_id: int, session: Session = Depends(get_session)):
    customer = Customer(id=customer_id).db_read(session=session)
    return JSONResponse(
        status_code=status.HTTP_200_OK, content={"message": f"Customer {customer_id} successfully loaded", "customer_info": customer.dict()}
    )


@router.post("/{customer_id}", response_model=CustomerRead)
def login_customer(customer_id: int, session: Session = Depends(get_session)):
    pass


@router.delete("/{customer_id}")
def delete_customer(customer_id: int, session: Session = Depends(get_session)):
    Customer(id=customer_id).db_delete(session=session)
    return JSONResponse(status_code=status.HTTP_200_OK, content={"message": f"Customer {customer_id} successfully deleted"})
