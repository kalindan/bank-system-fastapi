from fastapi import APIRouter, Depends, status
from fastapi.responses import JSONResponse
from app.auth.oauth2 import get_current_customer
from app.db import Session, get_session
from app.models import (
    Account,
    AccountWrite,
    AccountResponse,
    Limits,
    TransactionWrite,
    Transaction,
)
from app.models.customer_model import Customer
from app.models.transaction_model import TransactionType
from app.utils.messages import ACCOUNT_CREATED, ACCOUNT_LOADED

router = APIRouter(prefix="/accounts", tags=["accounts"])


@router.post(
    "/", response_model=AccountResponse, status_code=status.HTTP_201_CREATED
)
def register_account(
    account_write: AccountWrite,
    customer: Customer = Depends(get_current_customer),
    session: Session = Depends(get_session),
):
    account = (
        Account.from_orm(account_write)
        .set_customer_id(id=customer.id)
        .db_create(session=session)
        .get_response_model(
            status=status.HTTP_201_CREATED, message=ACCOUNT_CREATED
        )
    )
    return account


@router.get("/{account_id}", response_model=AccountResponse)
def get_account(
    account_id: int,
    customer: Customer = Depends(get_current_customer),
    session: Session = Depends(get_session),
):
    account = (
        Account(id=account_id)
        .db_check_ownership(customer_id=customer.id, session=session)
        .get_response_model(status=status.HTTP_200_OK, message=ACCOUNT_LOADED)
    )
    return account


@router.put("/{account_id}/limits")
def update_limits(
    account_id: int,
    limits: Limits,
    customer: Customer = Depends(get_current_customer),
    session: Session = Depends(get_session),
):
    account = (
        Account(id=account_id)
        .db_check_ownership(customer_id=customer.id, session=session)
        .db_update_limits(session=session, limits=limits)
    )
    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content={
            "message": f"Account {account.id} limits successfully updated",
            "daily_limit": account.daily_limit,
            "num_of_withdrawals": account.num_of_withdrawals,
        },
    )


@router.delete("/{account_id}")
def delete_account(
    account_id: int,
    customer: Customer = Depends(get_current_customer),
    session: Session = Depends(get_session),
):
    Account(id=account_id).db_check_ownership(
        customer_id=customer.id, session=session
    ).db_delete(session=session)
    Transaction(account_id=account_id).db_delete_all(session=session)
    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content={"message": f"Account {account_id} successfully deleted"},
    )


@router.put("/{account_id}/withdrawal")
def withdraw_money(
    account_id: int,
    transaction: TransactionWrite,
    customer: Customer = Depends(get_current_customer),
    session: Session = Depends(get_session),
):
    Account(id=account_id).db_check_ownership(
        customer_id=customer.id, session=session
    ).check_balance(
        amount=transaction.amount
    ).check_daily_withdrawals().check_amount_withdrawn(
        amount=transaction.amount
    ).db_update_balance(
        session=session, amount=-transaction.amount
    )
    Transaction(
        account_id=account_id,
        transaction_type=TransactionType.WITHDRAWAL,
        amount=transaction.amount,
    ).db_create(session=session)
    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content={
            "message": f"Successfully withdrawn {transaction.amount} CZK from account {account_id}"
        },
    )


@router.put("/{account_id}/deposit")
def deposit_money(
    account_id: int,
    transaction: TransactionWrite,
    customer: Customer = Depends(get_current_customer),
    session: Session = Depends(get_session),
):
    Account(id=account_id).db_check_ownership(
        customer_id=customer.id, session=session
    ).db_update_balance(session=session, amount=transaction.amount)
    Transaction(
        account_id=account_id,
        transaction_type=TransactionType.DEPOSIT,
        amount=transaction.amount,
    ).db_create(session=session)
    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content={
            "message": f"Successfully {transaction.amount} CZK deposited to account {account_id}"
        },
    )


@router.put("/{account_id}/transfer")
def transfer_money(
    account_id: int, session: Session = Depends(get_session)
):  # , account_to: Account, amount:int= Body()):
    pass
