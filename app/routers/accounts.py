from app.db import Session, crud_account, crud_transaction, get_session
from app.models import AccountRead, Limits, TransactionWrite
from app.models.transaction_model import TransactionType
from app.utils import (check_amount_withdrawn, check_balance,
                       check_daily_withdrawals)
from fastapi import APIRouter, Body, Depends

router=APIRouter(prefix="/accounts",
                 tags=["accounts"])

@router.post("/", response_model=AccountRead)
def register_account(session: Session = Depends(get_session)):
    customer_id: int = 1  # temporary until authentication is added
    return crud_account.create(session=session, customer_id=customer_id)


@router.delete("/{account_id}")
def delete_account(account_id: int, session: Session = Depends(get_session)):
    crud_transaction.delete_all(session=session, account_id=account_id)
    return crud_account.delete(session=session, account_id=account_id)


@router.get("/{account_id}", response_model=AccountRead)
def get_account(account_id: int, session: Session = Depends(get_session)):
    return crud_account.read(session=session, account_id=account_id)


@router.put("/{account_id}/limits")
def set_limits(account_id: int, limits: Limits, session: Session = Depends(get_session)):
    return crud_account.update_limits(session=session, account_id=account_id, limits=limits)


@router.put("/{account_id}/withdrawal")
def withdraw_money(account_id: int, transaction: TransactionWrite, session: Session = Depends(get_session)):
    account = crud_account.read(session=session, account_id=account_id)
    check_balance(account=account,amount=transaction.amount)
    transactions = crud_transaction.read_all(session=session, account_id=account_id)
    check_daily_withdrawals(account=account,transactions=transactions)
    check_amount_withdrawn(account=account,amount=transaction.amount,transactions=transactions)
    crud_account.update_balance(session=session,account_id=account_id,amount=-transaction.amount)
    crud_transaction.create(session=session, account_id=account_id, transaction_type=TransactionType.WITHDRAWAL, amount=transaction.amount)
    return {"status":"success",
            "message": f"Here is your {transaction.amount} CZK"}
    
@router.put("/{account_id}/deposit")
def deposit_money(account_id: int, transaction: TransactionWrite, session: Session = Depends(get_session)):
    crud_account.update_balance(session=session,account_id=account_id,amount=transaction.amount)
    crud_transaction.create(session=session, account_id=account_id, transaction_type=TransactionType.DEPOSIT, amount=transaction.amount)
    return {"status":"success",
            "message": f"{transaction.amount} CZK deposited to account {account_id}"}

@router.put("/{account_id}/transfer")
def transfer_money(account_id: int, session: Session = Depends(get_session)): #, account_to: Account, amount:int= Body()):
    pass
