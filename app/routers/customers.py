from fastapi import APIRouter, Depends, status
from fastapi.responses import JSONResponse
from app.db import get_session, Session
from app.models import Customer, CustomerWrite, CustomerRead, CustomerResponse
from app.utils.messages import CUSTOMER_CREATED, CUSTOMER_LOADED
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
        .db_check_by_email(session=session)
        .hash_password(customer_write.password)
        .db_create(session=session)
        .get_response_model(
            status=status.HTTP_201_CREATED, message=CUSTOMER_CREATED
        )
    )
    return customer


@router.get("/", response_model=CustomerResponse)
def customer_info(customer: Customer = Depends(get_current_customer)):
    return customer.get_response_model(
        status=status.HTTP_200_OK, message=CUSTOMER_CREATED
    )


@router.delete("/")
def delete_customer(
    customer: Customer = Depends(get_current_customer),
    session: Session = Depends(get_session),
):
    customer.db_delete(session=session)
    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content={"message": f"Customer {customer.id} successfully deleted"},
    )
