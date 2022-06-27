from fastapi import HTTPException
from .database import Session
from ..models import Account, Customer, Limits

class CRUDTransaction():
    @staticmethod
    def create(session: Session, account_id: int):
        pass
    
crud_transaction = CRUDTransaction()