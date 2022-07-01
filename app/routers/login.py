from app.auth.oauth2 import generate_token
from app.db import Session, get_session
from fastapi import APIRouter, Depends, status
from fastapi.security import OAuth2PasswordRequestForm
from app.models import Customer
from fastapi.responses import JSONResponse

router = APIRouter(prefix="/login", tags=["login"])


@router.post("")
def login_customer(
    login_form: OAuth2PasswordRequestForm = Depends(),
    session: Session = Depends(get_session),
):
    customer = (
        Customer(email=login_form.username)
        .db_read_by_email(session=session)
        .verify_password(password=login_form.password)
    )
    jwt = generate_token(customer_id=customer.id)
    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content={
            "message": f"Customer {customer.id} successfully authenticated",
            "access_token": jwt,
            "token_type": "Bearer",
        },
    )
