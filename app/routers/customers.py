from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import JSONResponse
from app.db import get_session, Session
from app.models import Customer, CustomerWrite, CustomerRead, CustomerResponse
from app.utils.enums import Messages as msg
from app.auth.oauth2 import get_current_customer

router = APIRouter(prefix="/customers", tags=["customers"])


@router.post(
    "/", response_model=CustomerResponse, status_code=status.HTTP_201_CREATED
)
def register_customer(
    customer_write: CustomerWrite, session: Session = Depends(get_session)
):
    customer = (
        Customer.from_orm(customer_write)
        .db_check_if_exists(session=session)
        .hash_password(customer_write.password)
        .db_create(session=session)
        .get_response_model(
            status=status.HTTP_201_CREATED, message=msg.CUSTOMER_CREATED
        )
    )
    return customer


@router.get("/{customer_id}", response_model=CustomerResponse)
def customer_info(
    customer_id: int, customer: Customer = Depends(get_current_customer)
):
    if customer_id != customer.id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Not authorized to view this customer profile",
        )
    return customer.get_response_model(
        status=status.HTTP_200_OK, message=msg.CUSTOMER_LOADED
    )


@router.delete("/{customer_id}")
def delete_customer(
    customer_id: int,
    customer: Customer = Depends(get_current_customer),
    session: Session = Depends(get_session),
):
    if customer_id != customer.id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Not authorized to delete this customer profile",
        )
    customer.db_delete(session=session)
    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content={"message": f"Customer {customer.id} successfully deleted"},
    )
