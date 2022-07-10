from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from datetime import datetime, timedelta
from app.config.config import active_config
from jose import JWTError, jwt  # type:ignore
from ..db import Session, get_session
from app.models.customer_model import Customer


ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 1

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")


def generate_token(customer_id: int):
    to_encode: dict = {"id": customer_id}
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(
        to_encode, active_config.secret_key, algorithm=ALGORITHM
    )
    return encoded_jwt


def get_current_customer(
    session: Session = Depends(get_session), token: str = Depends(oauth2_scheme)
):
    try:
        payload = jwt.decode(
            token, active_config.secret_key, algorithms=[ALGORITHM]
        )
        customer_id: int = payload.get("id")
        customer = Customer(id=customer_id).db_read_by_id(session=session)
        if customer is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Customer not found",
            )
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
        )
    return customer
