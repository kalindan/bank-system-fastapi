from fastapi import APIRouter, Depends, status
from fastapi.responses import JSONResponse
from app.db import Session, get_session
from app.models import AccountWrite, AccountRead, Limits, TransactionWrite, Transaction
from app.models.account_model import Account
from app.models.transaction_model import TransactionType


router = APIRouter(prefix="/accounts", tags=["accounts"])


@router.post("/")
def register_account(account_write: AccountWrite, session: Session = Depends(get_session)):
    customer_id: int = 1  # temporary until authentication is added
    account = Account.from_orm(account_write).set_customer_id(id=customer_id).db_create(session=session).get_read_model()
    return JSONResponse(
        status_code=status.HTTP_201_CREATED, content={"message": f"Account {account.id} successfully registered", "account_info": account}
    )


@router.get("/{account_id}")
def get_account(account_id: int, session: Session = Depends(get_session)):
    account = Account(id=account_id).db_read(session=session).get_read_model()
    return JSONResponse(status_code=status.HTTP_200_OK, content={"message": f"Account {account.id} successfully loaded", "account_info": account})


@router.put("/{account_id}/limits")
def update_limits(account_id: int, limits: Limits, session: Session = Depends(get_session)):
    account = Account(id=account_id).db_update_limits(session=session, limits=limits)
    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content={
            "message": f"Account {account.id} limits successfully updated",
            "daily_limit": account.daily_limit,
            "num_of_withdrawals": account.num_of_withdrawals,
        },
    )


@router.delete("/{account_id}")
def delete_account(account_id: int, session: Session = Depends(get_session)):
    Account(id=account_id).db_delete(session=session)
    Transaction(account_id=account_id).db_delete_all(session=session)
    return JSONResponse(status_code=status.HTTP_200_OK, content={"message": f"Account {account_id} successfully deleted"})


@router.put("/{account_id}/withdrawal")
def withdraw_money(account_id: int, transaction: TransactionWrite, session: Session = Depends(get_session)):
    Account(id=account_id).db_read(session=session).check_balance(amount=transaction.amount).check_daily_withdrawals().check_amount_withdrawn(
        amount=transaction.amount
    ).db_update_balance(session=session, amount=-transaction.amount)
    Transaction(account_id=account_id, transaction_type=TransactionType.WITHDRAWAL, amount=transaction.amount).db_create(session=session)
    return JSONResponse(
        status_code=status.HTTP_200_OK, content={"message": f"Successfully withdrawn {transaction.amount} CZK from account {account_id}"}
    )


@router.put("/{account_id}/deposit")
def deposit_money(account_id: int, transaction: TransactionWrite, session: Session = Depends(get_session)):
    Account(id=account_id).db_update_balance(session=session, amount=transaction.amount)
    Transaction(account_id=account_id, transaction_type=TransactionType.DEPOSIT, amount=transaction.amount).db_create(session=session)
    return JSONResponse(
        status_code=status.HTTP_200_OK, content={"message": f"Successfully {transaction.amount} CZK deposited to account {account_id}"}
    )


@router.put("/{account_id}/transfer")
def transfer_money(account_id: int, session: Session = Depends(get_session)):  # , account_to: Account, amount:int= Body()):
    pass
