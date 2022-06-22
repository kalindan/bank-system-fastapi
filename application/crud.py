from fastapi import HTTPException
from .database import Session
from .models import Account, Customer
from .schemas import Limits


class CRUDCustomer:
    @staticmethod
    def create(session: Session, customer: Customer) -> Customer:
        session.add(customer)
        session.commit()
        session.refresh(customer)
        return customer

    @staticmethod
    def read(session: Session, customer_id: int) -> Customer:
        customer = session.get(Customer, customer_id)
        if not customer:
            raise HTTPException(status_code=404, detail="Customer not found")
        return customer

    @staticmethod
    def delete(session: Session, customer_id: int) -> dict:
        customer = session.get(Customer, customer_id)
        if not customer:
            raise HTTPException(status_code=404, detail="Customer not found")
        session.delete(customer)
        session.commit()
        return {"message": f"Customer {customer_id} successfully deleted"}


class CRUDAccount:
    @staticmethod
    def create(session: Session, customer_id: int) -> Account:
        customer = session.get(Customer, customer_id)
        if not customer:
            raise HTTPException(status_code=404, detail="Customer not found")
        account = Account(customer_id=customer_id)
        session.add(account)
        session.commit()
        session.refresh(account)
        return account

    @staticmethod
    def read(session: Session, account_id: int) -> Account:
        account = session.get(Account, account_id)
        if not account:
            raise HTTPException(status_code=404, detail="Account not found")
        return account

    @staticmethod
    def update_balance(session: Session, account_id: int, amount: float) -> Account:
        account = session.get(Account, account_id)
        if not account:
            raise HTTPException(status_code=404, detail="Account not found")
        account.balance += amount
        session.add(account)
        session.commit()
        session.refresh(account)
        return account

    @staticmethod
    def update_limits(session: Session, account_id: int, limits: Limits) -> Account:
        account = session.get(Account, account_id)
        if not account:
            raise HTTPException(status_code=404, detail="Account not found")
        account.daily_limit = limits.daily_limit
        account.num_of_withdrawals = limits.num_of_withdrawals
        session.add(account)
        session.commit()
        session.refresh(account)
        return account

    @staticmethod
    def delete(session: Session, account_id: int) -> dict:
        account = session.get(Account, account_id)
        if not account:
            raise HTTPException(status_code=404, detail="Account not found")
        session.delete(account)
        session.commit()
        return {"message": f"Account {account_id} successfully deleted"}


crud_customer = CRUDCustomer()
crud_account = CRUDAccount()
