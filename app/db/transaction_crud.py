from fastapi import HTTPException
from sqlmodel import select
from app.models.transaction_model import TransactionType, Transaction
from app.models import Account
from .database import Session

class CRUDTransaction():
    @staticmethod
    def create(session: Session, account_id: int, transaction_type:TransactionType, amount:float):
        account = session.get(Account, account_id)
        if not account:
            raise HTTPException(status_code=404, detail="Account not found")
        transaction = Transaction(amount=amount,transaction_type=transaction_type,account_id=account_id)
        session.add(transaction)
        session.commit()
        session.refresh(transaction)
        return
    
    @staticmethod
    def read_all(session: Session, account_id: int):
        transactions = session.exec(select(Transaction).where(Transaction.account_id==account_id))
        return transactions
    
    @staticmethod
    def delete_all(session: Session, account_id: int) -> dict:
        transactions = session.exec(select(Transaction).where(Transaction.account_id==account_id))
        for transaction in transactions:
            session.delete(transaction)
        session.commit()
        return {"status":"success",
                "message": f"Account {account_id} transactions successfully deleted"}
    
crud_transaction = CRUDTransaction()