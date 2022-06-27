
from datetime import datetime
from fastapi import HTTPException, status

from ..models.transaction_model import TransactionType
from ..models.account_model import Account


def check_balance(account:Account, amount:float):
    if account.balance < amount:
        raise HTTPException(status_code=status.HTTP_406_NOT_ACCEPTABLE,detail="Not sufficient balance")

def check_daily_withdrawals(account:Account, transactions):
    withdrawals_today = len([transaction for transaction in transactions if transaction.date.date() == datetime.now().date() and transaction.transaction_type == TransactionType.WITHDRAWAL])
    if account.num_of_withdrawals <= withdrawals_today:
        raise HTTPException(status_code=status.HTTP_406_NOT_ACCEPTABLE,detail="No more allowed withdrawals today")
    
def check_amount_withdrawn(account:Account, amount:float, transactions):
    withdrawn_today = sum([transaction.amount for transaction in transactions if transaction.date.date() == datetime.now().date() and transaction.transaction_type == TransactionType.WITHDRAWAL])
    if amount > account.daily_limit - withdrawn_today:
        raise HTTPException(status_code=status.HTTP_406_NOT_ACCEPTABLE,detail="Desired amount over allowed daily limit")